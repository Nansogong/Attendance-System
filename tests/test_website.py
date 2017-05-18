import pytest
from flask import session

from app import app

from views import website


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
