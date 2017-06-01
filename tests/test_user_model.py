import pytest
import sys


def test_set_check_password():
    from models.user import User

    password = 'skagustlfqkqh'
    user = User(user_num=12321312, name='JS Han', email='test@test.com', password=password, fingerprint='12321', type=User.STUDENT_TYPE)
    assert user.check_password(password)


def test_create_user():
    from models.user import User
    password = 'skagustlfqkqh'
    user = User(user_num=12321312, name='JS Han', email='test@test.com', password=password, fingerprint='12321', type=User.STUDENT_TYPE)

    user.create()
    assert user.id > 0


def test_find_user_by_email():
    from models.user import User
    email = 'test@test.com'
    user = User.find_by_email(email=email)

    assert user.email == 'test@test.com'


def test_find_by_email_and_password():
    from models.user import User

    email = 'test@test.com'
    password = 'skagustlfqkqh'

    user = User.find_by_email_and_password(email=email, password=password)

    assert user.email == email
    assert user.check_password(password)
