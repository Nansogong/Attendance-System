import pytest


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


def create_user_first():
@pytest.fixture(scope='session')
    from models.user import User
    password = 'alskdjfhghfj'
    user = User(user_num=1234321, name='Pro fessor', email='professor@professor.com', password=password,
                fingerprint='13531', type=User.PROFESSOR_TYPE)
    user.create()
    yield user
