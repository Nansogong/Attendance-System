from datetime import datetime

from flask import current_app
from sqlalchemy.dialects.mysql import INTEGER, TINYINT

from models import db

db.init_app(current_app)


class Lecture(db.Model):
    __tablename__ = 'lecture'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    professor_id = db.Column(INTEGER(unsigned=True), db.ForeignKey("user.id"))  # user_id 인데 명확하게 표현하기위해서 이름을 바꿈.
    name = db.Column(db.String(255))
    lecture_code = db.Column(db.String(255))
    criteria_of_F = db.Column(TINYINT(unsigned=True), default=3)
    created = db.Column(db.DateTime(), default=datetime.now(), index=True)

    def __init__(self, professor_id, name, lecture_code, criteria_of_F=3):
        self.professor_id = professor_id
        self.name = name
        self.lecture_code = lecture_code
        self.criteria_of_F = criteria_of_F

    def create(self):
        db.session.add(self)
        db.session.commit()
        return True


class LectureDay(db.Model):
    __tablename__ = 'lecture_day'

    MON = 1
    TUE = 2
    WED = 3
    TEU = 4
    FRI = 5
    SAT = 6

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    lecture_id = db.Column(INTEGER(unsigned=True), db.ForeignKey("lecture.id"))
    start = db.Column(db.Time)
    time = db.Column(INTEGER(unsigned=True))
    day = db.Column(TINYINT(unsigned=True))

    def __init__(self, start, time, day, lecture_id):
        self.start = start
        self.time = time
        self.day = day
        self.lecture_id = lecture_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return True


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
