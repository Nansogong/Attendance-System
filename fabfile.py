from pprint import pprint

import os
from fabric.context_managers import cd, settings, prefix
from fabric.decorators import task, roles

from fabric.operations import local, run
from fabric.state import env
from fabric.tasks import execute
from flask_sqlalchemy import SQLAlchemy

import config
from app import app
db = SQLAlchemy(app)


basedir = os.path.abspath(os.path.dirname(__file__))
env_name = 'local'

env.roledefs = {
    'localhost': ['localhost'],
    'develop': {
        'hosts': ['{}@{}'.format(config.DevelopConfig.REMOTE["user"], config.DevelopConfig.REMOTE["hosts"][0])],
    },
    'live': {
        'hosts': ['{}@{}'.format(config.LiveConfig.REMOTE["user"], config.LiveConfig.REMOTE["hosts"][0])],
    }
}

config_instance = config.LocalConfig
env_name = 'local'


# TODO: 스탑서버 리모트 디플로이 테스트

def set_env(specific_configuration):
    for key, value in specific_configuration.REMOTE.items():
        env[key] = value


@task
def localhost():
    global config_instance, env_name
    env_name = 'local'
    config_instance = config.LocalConfig
    set_env(config_instance)


@task
def develop():
    global config_instance, env_name
    env_name = 'develop'
    config_instance = config.DevelopConfig
    set_env(config_instance)


@task
def live():
    global config_instance, env_name
    env_name = 'live'
    config_instance = config.LiveConfig
    set_env(config_instance)


@task(alias='run')
def runserver():
    if env_name == 'local':
        local('python app.py')  # local을 덮어씌우면 아래는 로컬로 실행될 듯.
        return
    run('service {} stop'.format(config_instance.SERVICE_NAME))
    run('service {} start'.format(config_instance.SERVICE_NAME))


@task(alias='stop')
def stop_server():
    if env_name == 'local':
        return
    run('service {} stop'.format(config_instance.SERVICE_NAME))


@task
def init_db():
    import models.user, models.lecture

    if env_name is not 'local':
        with cd('Attendance-System'), prefix('source venv/bin/activate'):
            run('fab {} init_db'.format(env_name))
    pprint(db)
    db.drop_all()
    db.create_all()


@task
def deploy():
    with settings(warn_only=True):
        with cd('Attendance-System'), prefix('source venv/bin/activate'):
            global env_name
            env_name = 'master' if env_name == 'live' else env_name
            run('git checkout -b {}'.format(env_name))
            run('git pull origin {}'.format(env_name))
            run('pip install -r requirements.txt')
            runserver()


@task
@roles('localhost')
def test():
    with settings(warn_only=True):
        with prefix('source venv/bin/activate'):
            local('pytest tests/')
