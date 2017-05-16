import pytest
from app import app  # 지우지 말 것


def test_set_check_password():
    from models.user import User

    password = 'skagustlfqkqh'
    user = User(user_num=12321312, name='JS Han', email='test@test.com', password=password, fingerprint='12321', type=1)
    assert user.check_password(password)


def test_create_user(session):
    from models.user import User
    password = 'skagustlfqkqh'
    user = User(user_num=12321312, name='JS Han', email='test@test.com', password=password, fingerprint='12321', type=1)

    assert user.create()


