from datetime import datetime

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import INTEGER, TINYINT

from app import app

db = SQLAlchemy(app)


class Lecture(db.Model):
    __tablename__ = 'lecture'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    professor_id = db.Column(INTEGER(unsigned=True))  # user_id 인데 명확하게 표현하기위해서 이름을 바꿈.
    name = db.Column(db.String(255))
    lecture_code = db.Column(db.String(255))
    lecture_day_id = db.Column(INTEGER(unsigned=True))
    criteriaOfF = db.Column(TINYINT(unsigned=True))
    created = db.Column(db.DateTime(), default=datetime.now(), index=True)


class LectureDay(db.Model):
    __tablename__ = 'lecture_day'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    start = db.Column(db.DateTime)
    time = db.Column(INTEGER(unsigned=True))
    day = db.Column(TINYINT(unsigned=True))


class AttendanceManagement(db.Model):
    __tablename__ = 'attendance_management'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    user_id = db.Column(INTEGER(unsigned=True))
    lecture_id = db.Column(INTEGER(unsigned=True))
    is_checked = db.Column(TINYINT(unsigned=True))
    created = db.Column(db.DateTime(), default=datetime.now(), index=True)


class StudentLecture(db.Model):
    __tablename__ = 'student_lecture'

    student_id = db.Column(INTEGER(unsigned=True), db.ForeignKey("user.id"), primary_key=True)
    lecture_id = db.Column(INTEGER(unsigned=True), db.ForeignKey("lecture.id"), primary_key=True)
    accept_status = db.Column(TINYINT(unsigned=True))
    updated = db.Column(db.DateTime())
    created = db.Column(db.DateTime(), default=datetime.now())
