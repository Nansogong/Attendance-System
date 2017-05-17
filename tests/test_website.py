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


def test_login_post():
    with app.test_client() as mod:

        email = 'test@test.com'
        password = 'skagustlfqkqh'
        res = mod.post('login', data=dict(
            email=email,
            password=password
        ))

        # TODO: 세션이 생성 됐는지 확인
        assert session.get('email') == email
        assert res.status_code == 200
