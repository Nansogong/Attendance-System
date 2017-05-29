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
        assert b'user_num' not in res.data
        assert b'name' not in res.data
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


def test_create_lecture_success(user):
# def test_create_lecture_success(user):
#     with app.test_client() as mod:
#         professor_id = user.id
#         name = 'Computer Structure'
#         lecture_code = 20543
#         start = '14:30'
#         time = 90
#         day = 2
#
#         res = mod.post('/lectures/create', data=dict(
#             professor_id=professor_id,
#             name=name,
#             lecture_code=lecture_code,
#             start=start,
#             time=time,
#             day=day
#         ), follow_redirects=True)
#
#         assert b'list' in res.data
#         assert b'profile' in res.data
#         assert b'logout' in res.data
#
#
# def test_create_lecture_blank_fail(user):
#     with app.test_client() as mod:
#         professor_id = user.id
#         name = ''
#         lecture_code = 20543
#         start = '14:30'
#         time = 90
#         day = 2
#
#         res = mod.post('create_lecture', data=dict(
#             name=name,
#             lecture_code=lecture_code,
#             start=start,
#             time=time,
#             day=day
#         ), follow_redirects=True)
#
#         assert b'name' in res.data
#         assert b'lecture_code' in res.data
#         assert b'start' in res.data
#         assert b'time' in res.data
#         assert b'lab' not in res.data
#         assert b'logout' not in res.data
#
#
# def test_create_lecture_not_professor_fail(user):
#     with app.test_client() as mod:
#         professor_id = user.id
#         name = 'Computer Architecture'
#         lecture_code = 20543
#         start = '14:30'
#         time = 90
#         day = 2
#
#         res = mod.post('create_lecture', data=dict(
#             professor_id=professor_id,
#             name=name,
#             lecture_code=lecture_code,
#             start=start,
#             time=time,
#             day=day
#         ), follow_redirects=True)
#
#         assert b'list' in res.data
#         assert b'logout' in res.data
#         assert b'profile' in res.data
#         assert b'lecture_code' not in res.data
#         assert b'start' not in res.data
#         assert b'time' not in res.data
    with app.test_client() as mod:
        professor_id = user.id
        name = 'Computer Structure'
        lecture_code = 20543
        start = '14:30'
        time = 90
        day = 2

        res = mod.post('/lectures/create', data=dict(
            professor_id=professor_id,
            name=name,
            lecture_code=lecture_code,
            start=start,
            time=time,
            day=day
        ), follow_redirects=True)

        assert b'list' in res.data
        assert b'profile' in res.data
        assert b'logout' in res.data


def test_create_lecture_blank_fail(user):
    with app.test_client() as mod:
        professor_id = user.id
        name = ''
        lecture_code = 20543
        start = '14:30'
        time = 90
        day = 2

        res = mod.post('create_lecture', data=dict(
            name=name,
            lecture_code=lecture_code,
            start=start,
            time=time,
            day=day
        ), follow_redirects=True)

        assert b'name' in res.data
        assert b'lecture_code' in res.data
        assert b'start' in res.data
        assert b'time' in res.data
        assert b'lab' not in res.data
        assert b'logout' not in res.data


def test_create_lecture_not_professor_fail(user):
    with app.test_client() as mod:
        professor_id = user.id
        name = 'Computer Architecture'
        lecture_code = 20543
        start = '14:30'
        time = 90
        day = 2

        res = mod.post('create_lecture', data=dict(
            professor_id=professor_id,
            name=name,
            lecture_code=lecture_code,
            start=start,
            time=time,
            day=day
        ), follow_redirects=True)

        assert b'list' in res.data
        assert b'logout' in res.data
        assert b'profile' in res.data
        assert b'lecture_code' not in res.data
        assert b'start' not in res.data
        assert b'time' not in res.data