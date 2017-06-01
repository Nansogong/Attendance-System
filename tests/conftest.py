import pytest
from app import app
from models.user import User


@pytest.fixture(scope='session', autouse=True)
def session():
    from models.user import db

    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session
    yield
    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture(scope='session')
def mod():
    """
    플라스크 test client를 생성합니다 이 fixture를 사용하면 with statement안에 생성된 test client를 사용할 수 있습니다.
    :rtype: flask.app
    """
    with app.test_client() as mod:
        yield mod


@pytest.fixture(scope='session', params=[
    dict(email="test_login_professor@professor.com", password="alskdjfhghfj", user_type=User.PROFESSOR_TYPE),
    dict(email="test_login_ta@ta.com", password="alskdjfhghfj", user_type=User.TA_TYPE),
    dict(email="test_login_student@student.com", password="alskdjfhghfj", user_type=User.STUDENT_TYPE)])
def login_user(request, mod):
    """
    3가지의 유저 형태로 로그인을 합니다. 로그인할 유저는 로그인시에 생성해주며 그유저로 액션을 하면 됩니다.
    각 유저의 정보는 params 에 담겨오며 접근은 request.param으로 할 수 있습니다.
    flask app은 상단 mod method에서 생성되어 내려옵니다.
    :param request: 상단에 선언된 dict중 1개가 순서대로 실행됩니다. request.param으로 접근 가능합니다
    :param mod: mod() fixture 에서 생성된 flask.app 입니다
    :rtype: User
    """
    from random import randint
    from flask import session as sess

    _user = User(user_num=randint(0, 100000), name='Pro fessor', email=request.param['email'],
                 password=request.param['password'],
                 fingerprint='13531', type=request.param['user_type'])
    _user.create()
    res = mod.post('login', data=dict(
        email=request.param['email'],
        password=request.param['password']
    ), follow_redirects=True)
    yield _user


@pytest.fixture(scope='session')
def lecture(user):
    from models.lecture import Lecture
    _lecture = Lecture(professor_id=user.id, name="SWE", lecture_code="12364")
    _lecture.create()
    yield _lecture
