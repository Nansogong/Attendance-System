from datetime import datetime
from flask import current_app
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from werkzeug.security import generate_password_hash, check_password_hash

from models import db

db.init_app(current_app)


class User(db.Model):
    __tablename__ = 'user'
    PROFESSOR_TYPE = 1
    STUDENT_TYPE = 2
    TA_TYPE = 3

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    user_num = db.Column(INTEGER(unsigned=True))  # 학생 번호나 교수님 고유 코드. 실제로 중복되는지 알 수 없어서 유니크 제외. view만 할 듯
    name = db.Column(db.Text)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.Text)
    fingerprint = db.Column(db.String(255))
    lab_id = db.Column(INTEGER(unsigned=True), db.ForeignKey("lab.id"))
    type = db.Column(TINYINT(unsigned=True))  # 교수님인지 학생인지 TA인지.. 승인전인지 승인 된건지..!
    created = db.Column(db.DateTime(), default=datetime.now(), index=True)

    def __init__(self, user_num, name, email, password, fingerprint, type):
        self.user_num = user_num
        self.name = name
        self.email = email
        self.set_password(password)
        self.fingerprint = fingerprint
        self.type = type

    # http://flask.pocoo.org/snippets/54/
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return True

    def __repr__(self):
        return '<User %d>' % self.user_num

    @classmethod
    def find_by_user_num(cls, user_num):
        return cls.query.filter_by(user_num=user_num).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_email_and_password(cls, email, password):
        user = cls.find_by_email(email)
        if not user:
            return None
        if not user.check_password(password):
            return None
        return user


class Lab(db.Model):
    __tablename__ = 'lab'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    description = db.Column(db.Text)
    office_hour = db.Column(db.String(255))
    created = db.Column(db.DateTime(), default=datetime.now(), index=True)
