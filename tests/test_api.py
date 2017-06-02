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


def test_find_by_email_true(user):
    with app.test_client() as mod:
        from flask import json
        email = 'professor@professor.com'
        res = mod.post('find_by_email', data=dict(
            email=email
        ), follow_redirects=True)

        data = json.loads(res.data)

        assert data['user_exist'] == True


def test_find_by_email_false(user):
    with app.test_client() as mod:
        from flask import json
        email = 'asdf@asdf.com'
        res = mod.post('find_by_email', data=dict(
            email=email
        ), follow_redirects=True)

        data = json.loads(res.data)

        assert data['user_exist'] == False


def test_professor_list_get(professors):
    from flask import json
    mod = app.test_client()
    res = mod.get('professor_list')

    list = json.loads(res.data)
    assert list['list'] == [
        {'email': 'professor@professor.com', 'name': 'Pro fessor', 'status': 1, 'user_num': 1234321},
        {'email': 'professor1@professor.com', 'name': 'Pro fessor1', 'status': 1, 'user_num': 2345432},
        {'email': 'professor2@professor.com', 'name': 'Pro fessor2', 'status': 8, 'user_num': 3456543},
        {'email': 'professor3@professor.com', 'name': 'Pro fessor3', 'status': 16, 'user_num': 5678765}]


def test_accept_professor_post_success_accept(professors):
    with app.test_client() as mod:
        from flask import json
        email = 'professor1@professor.com'
        status = 'accept'
        res = mod.post('accept_professor', data=dict(
            email=email,
            status=status
        ), follow_redirects=True)

        data = json.loads(res.data)
        assert data['status'] == 8


def test_accept_professor_post_success_reject(professors):
    with app.test_client() as mod:
        from flask import json
        email = 'professor1@professor.com'
        status = 'reject'
        res = mod.post('accept_professor', data=dict(
            email=email,
            status=status
        ), follow_redirects=True)

        data = json.loads(res.data)
        assert data['status'] == 16


def test_accept_professor_post_success_cancel(professors):
    with app.test_client() as mod:
        from flask import json
        email = 'professor1@professor.com'
        status = 'cancel'
        res = mod.post('accept_professor', data=dict(
            email=email,
            status=status
        ), follow_redirects=True)

        data = json.loads(res.data)
        assert data['status'] == 1


def test_accept_professor_post_request_error(professors):
    with app.test_client() as mod:
        from flask import json
        email = 'professor1@professor.com'
        status = 'asdf'
        res = mod.post('accept_professor', data=dict(
            email=email,
            status=status
        ), follow_redirects=True)

        data = json.loads(res.data)
        assert data['status'] == 'request_error'


def test_accept_professor_post_fail(professors):
    with app.test_client() as mod:
        from flask import json
        email = 'asdf@asdf.com'
        status = 'accept'
        res = mod.post('accept_professor', data=dict(
            email=email,
            status=status
        ), follow_redirects=True)

        data = json.loads(res.data)
        assert data['msg'] == 'user_not_exist'
