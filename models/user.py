from datetime import datetime

from sqlalchemy.dialects.mysql import INTEGER, TINYINT

from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    user_num = db.Column(INTEGER(unsigned=True))  # 학생 번호나 교수님 고유 코드. 실제로 중복되는지 알 수 없어서 유니크 제외. view만 할 듯
    name = db.Column(db.Text)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.Text)
    fingerprint = db.Column(db.String(255))
    lab_id = db.Column(INTEGER(unsigned=True), db.ForeignKey("lab.id"))
    type = db.Column(TINYINT(unsigned=True))  # 교수님인지 학생인지 TA인지.. 승인전인지 승인 된건지..!
    created = db.Column(db.DateTime(), default=datetime.now(), index=True)
    # TODO: password hashing


class Lab(db.Model):
    __tablename__ = 'lab'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    description = db.Column(db.Text)
    office_hour = db.Column(db.String(255))
    created = db.Column(db.DateTime(), default=datetime.now(), index=True)

