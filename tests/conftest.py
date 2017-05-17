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

