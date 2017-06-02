import pytest
import sys

from app import app
from flask import session
from views import website


def test_home():
    pass


def test_login_get(mod):
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


def test_logout():
    with app.test_client() as mod:
        email = 'test@test.com'
        password = 'skagustlfqkqh'

        res = mod.post('login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

        assert session.get('email', None)

        res = mod.get('logout', follow_redirects=True)
        assert res.status_code == 200
        assert not session.get('email', None)


def test_register_get(mod):
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


def test_create_lecture_get(mod, login_user):
    from models.user import User

    res = mod.get('/lectures/create', follow_redirects=True)

    if login_user.type == User.PROFESSOR_TYPE:
        assert res.status_code == 200
        assert b'create' in res.data
        assert b'lecture_code' in res.data
        assert b'time' in res.data
        assert b'start' in res.data

    if login_user.type != User.PROFESSOR_TYPE:
        assert res.status_code == 200
        assert b'list' in res.data
        assert b'profile' in res.data
        assert b'logout' in res.data


def test_create_lecture(mod, login_user):
    from models.lecture import LectureDay
    from models.user import User

    professor_id = login_user.id
    name = "Software Engineering"
    lecture_code = "40201"
    start = "10:30"
    time = 90
    day = LectureDay.MON

    res = mod.post('/lectures/create', data=dict(
        professor_id=professor_id,
        name=name,
        lecture_code=lecture_code,
        start=start,
        time=time,
        day=day
    ), follow_redirects=True)

    if login_user == User.PROFESSOR_TYPE:
        assert res.status_code == 200
        assert b'list' in res.data
        assert b'profile' in res.data
        assert b'logout' in res.data

    if login_user != User.PROFESSOR_TYPE:
        assert res.status_code == 200
        assert b'list' in res.data
        assert b'profile' in res.data
        assert b'logout' in res.data


def test_create_lecture_time_format_fail(mod, login_user):
    from models.lecture import LectureDay

    professor_id = login_user.id
    name = "Software Engineering"
    lecture_code = "40501"
    start = "10"
    time = 90
    day = LectureDay.MON

    res = mod.post('/lectures/create', data=dict(
        professor_id=professor_id,
        name=name,
        lecture_code=lecture_code,
        start=start,
        time=time,
        day=day
    ), follow_redirects=True)

    assert res.status_code == 200
    assert b'create' in res.data
    assert b'lecture_code' in res.data
    assert b'time' in res.data
    assert b'start' in res.data


def test_create_lecture_blank_fail(mod, login_user):
    from models.lecture import LectureDay

    professor_id = login_user.id
    name = ""
    lecture_code = ""
    start = ""
    time = 90
    day = LectureDay.MON

    res = mod.post('/lectures/create', data=dict(
        professor_id=professor_id,
        name=name,
        lecture_code=lecture_code,
        start=start,
        time=time,
        day=day
    ), follow_redirects=True)

    assert res.status_code == 200
    assert b'create' in res.data
    assert b'lecture_code' in res.data
    assert b'time' in res.data
    assert b'start' in res.data


def test_create_lecture_code_dup_fail(mod, login_user):
    from models.lecture import LectureDay

    professor_id = login_user.id
    name = "Logics"
    lecture_code = "40201"
    start = "15:00"
    time = 90
    day = LectureDay.WED

    res = mod.post('/lectures/create', data=dict(
        professor_id=professor_id,
        name=name,
        lecture_code=lecture_code,
        start=start,
        time=time,
        day=day
    ), follow_redirects=True)

    res = mod.post('/lectures/create', data=dict(
        professor_id=professor_id,
        name=name,
        lecture_code=lecture_code,
        start="14:30",
        time=time,
        day=day
    ), follow_redirects=True)

    assert res.status_code == 200
    assert b'create' in res.data
    assert b'lecture_code' in res.data
    assert b'time' in res.data
    assert b'start' in res.data