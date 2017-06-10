import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = 'nansogong-key'

    REMOTE = {
        "hosts": [""],
        "user": "",
        "password": ""
    }


class LocalConfig(Config):
    DEBUG = True


class DevelopConfig(Config):
    DEBUG = True


class LiveConfig(Config):
    pass
