import pytest
import sys

if sys.version_info >= (3, 6):
    try:
        from app import app  # 지우지 말 것
    except ModuleNotFoundError as e:
        import os
        myPath = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, myPath + '/../')
        from app import app
else:
    try:
        from app import app  # 지우지 말 것
    except ImportError as e:
        import os
        myPath = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, myPath + '/../')
        from app import app

from views import website
from flask import session


def test_home():
    pass


def test_login_get():
    mod = app.test_client()
    res = mod.get('login')

    assert res.status_code == 200
    assert b'email' in res.data
    assert b'password' in res.data


def test_login_post_success():
    with app.test_client() as mod:
        email = 'test@test.com'
        password = 'skagustlfqkqh'
        res = mod.post('login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

        assert session.get('email') == email
        assert res.status_code == 200


def test_login_post_success_admin():
    with app.test_client() as mod:
        email = 'nansogong'
        password = 'sksthrhd'
        res = mod.post('login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

        assert session.get('email') == 'admin'
        assert res.status_code == 200
        assert b'admin' in res.data
        assert b'accept_professor' in res.data


def test_login_post_fail():
    with app.test_client() as mod:
        email = 'test@test.com'
        password = '12345'

        res = mod.post('login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

        assert not session.get('email', None)
        assert b'email' in res.data
        assert b'password' in res.data


def test_register_get():
    mod = app.test_client()
    res = mod.get('register')

    assert res.status_code == 200
    assert b'user_num' in res.data
    assert b'name' in res.data
    assert b'email' in res.data
    assert b'password' in res.data


def test_register_post_success():
    with app.test_client() as mod:
        from models.user import User
        user_num = 2015000000
        name = 'Hsil Nam'
        email = 'hsilnam3@test.com'
        password = 'sksthrhd'
        fingerprint = '123456'
        type = 1

        res = mod.post('register', data=dict(
            user_num=user_num,
            name=name,
            email=email,
            password=password,
            fingerprint=fingerprint,
            type=type
        ), follow_redirects=True)

        assert res.status_code == 200
        assert b'email' in res.data
        assert b'password' in res.data
        assert not b'user_num' in res.data
        assert not b'name' in res.data
        assert User.find_by_email(email)
        assert User.find_by_user_num(user_num)


def test_register_post_overlap_fail():
    with app.test_client() as mod:

        user_num = 12321312  # 학번이 중복되었을 경우
        name = 'Hsil Nam'
        email = 'test@test.com'  # 이메일이 중복되었을 경우
        password = 'sksthrhd'
        fingerprint = '123456'
        type = 1

        res = mod.post('register', data=dict(
            user_num=user_num,
            name=name,
            email=email,
            password=password,
            fingerprint=fingerprint,
            type=type
        ), follow_redirects=True)

        assert b'email' in res.data
        assert b'password' in res.data
        assert b'user_num' in res.data
        assert b'name' in res.data


def test_register_post_blank_fail():
    with app.test_client() as mod:

        user_num = 2014
        name = ''
        email = 'fds'
        password = 'as'
        fingerprint = 'as'
        type = 1

        res = mod.post('register', data=dict(
            user_num=user_num,
            name=name,
            email=email,
            password=password,
            fingerprint=fingerprint,
            type=type
        ), follow_redirects=True)

        assert b'email' in res.data
        assert b'password' in res.data
        assert b'user_num' in res.data
        assert b'name' in res.data


def test_admin_get():
    mod = app.test_client()
    res = mod.get('admin')

    assert res.status_code == 200
    assert b'accept_professor' in res.data


def test_accept_professor_get():
    with app.test_client() as mod:
        res = mod.get('/accept_professor')
        assert b'professor' in res.data
        assert b'accept' in res.data
        assert b'reject' in res.data
        assert b'cancel' in res.data
