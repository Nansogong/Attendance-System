import pytest


@pytest.fixture(scope='session', autouse=True)
def session():
    from models.user import db

    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    _session = db.create_scoped_session(options=options)

    db.session = _session
    yield
    transaction.rollback()
    connection.close()
    _session.remove()


@pytest.fixture(scope='session')
def user():
    from models.user import User
    password = 'alskdjfhghfj'
    _user = User(user_num=1234321, name='Pro fessor', email='professor@professor.com', password=password,
                 fingerprint='13531', type=User.PROFESSOR_TYPE)
    _user.create()
    yield _user


@pytest.fixture(scope='session')
def lecture(user):
    from models.lecture import Lecture
    _lecture = Lecture(professor_id=user.id, name="SWE", lecture_code="12364")
    _lecture.create()
    yield _lecture


@pytest.fixture(scope='session')
def professors():
    from models.user import User
    password = 'asdfasdfasdf'
    _user = User(user_num=2345432, name='Pro fessor1', email='professor1@professor.com', password=password,
                 fingerprint='35753', type=User.PROFESSOR_TYPE)
    _user.create()
    password = 'sdfgsdfgsdfg'
    _user = User(user_num=3456543, name='Pro fessor2', email='professor2@professor.com', password=password,
                 fingerprint='56765', type=User.ACCEPTED_PROFESSOR_TYPE)
    _user.create()
    password = 'dfghdfghdfgh'
    _user = User(user_num=5678765, name='Pro fessor3', email='professor3@professor.com', password=password,
                 fingerprint='78987', type=User.REJECTED_PROFESSOR_TYPE)
    _user.create()
    yield
