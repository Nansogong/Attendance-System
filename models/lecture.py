from datetime import datetime

from flask import current_app
from sqlalchemy.dialects.mysql import INTEGER, TINYINT

from models import db

db.init_app(current_app)


class Lecture(db.Model):
    __tablename__ = 'lecture'

    SPRING = ['03', '04', '05']
    SUMMER = ['06', '07', '08']
    ANTUMN = ['09', '10', '11']
    WINTER = ['01', '02', '12']

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

    @classmethod
    def check_term(cls, user_date, lecture_code):
        from sqlalchemy import or_

        date = user_date.split('-')
        if date[1] in Lecture.SPRING:
            return cls.query.filter(or_(cls.created.like(date[0] + '-03-%'), cls.created.like(date[0] + '-04-%')),
                                    cls.lecture_code == lecture_code).first()

        elif date[1] in Lecture.SUMMER:
            return cls.query.filter(or_(cls.created.like(date[0] + '-06-%'), cls.created.like(date[0] + '-07-%')),
                                    cls.lecture_code == lecture_code).first()

        elif date[1] in Lecture.ANTUMN:
            return cls.query.filter(or_(cls.created.like(date[0] + '-09-%'), cls.created.like(date[0] + '-10-%')),
                                    cls.lecture_code == lecture_code).first()

        elif date[1] in Lecture.WINTER:
            return cls.query.filter(or_(cls.created.like(date[0] + '-12-%'), cls.created.like(date[0] + '-01-%')),
                                    cls.lecture_code == lecture_code).first()

    @classmethod
    def get_current_semester(cls):
        from sqlalchemy import or_
        import datetime

        user_date = str(datetime.datetime.now())
        date = user_date.split('-')
        if date[1] in Lecture.SPRING:
            return cls.query.filter(or_(cls.created.like(date[0] + '-03-%'), cls.created.like(date[0] + '-04-%'))).all()

        elif date[1] in Lecture.SUMMER:
            return cls.query.filter(or_(cls.created.like(date[0] + '-06-%'), cls.created.like(date[0] + '-07-%'))).all()

        elif date[1] in Lecture.ANTUMN:
            return cls.query.filter(or_(cls.created.like(date[0] + '-09-%'), cls.created.like(date[0] + '-10-%'))).all()

        elif date[1] in Lecture.WINTER:
            return cls.query.filter(or_(cls.created.like(date[0] + '-12-%'), cls.created.like(date[0] + '-01-%'))).all()

    @classmethod
    def get_my_current_lecture(cls, user_date, professor_id):
        from sqlalchemy import or_

        date = user_date.split('-')
        if date[1] in Lecture.SPRING:
            return cls.query.filter(or_(cls.created.like(date[0] + '-03-%'), cls.created.like(date[0] + '-04-%')),
                                    cls.professor_id == professor_id).first()

        elif date[1] in Lecture.SUMMER:
            return cls.query.filter(or_(cls.created.like(date[0] + '-06-%'), cls.created.like(date[0] + '-07-%')),
                                    cls.professor_id == professor_id).first()

        elif date[1] in Lecture.ANTUMN:
            return cls.query.filter(or_(cls.created.like(date[0] + '-09-%'), cls.created.like(date[0] + '-10-%')),
                                    cls.professor_id == professor_id).first()

        elif date[1] in Lecture.WINTER:
            return cls.query.filter(or_(cls.created.like(date[0] + '-12-%'), cls.created.like(date[0] + '-01-%')),
                                    cls.professor_id == professor_id).first()


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


class StudentAttendance(db.Model):
    __tablename__ = 'student_attendance'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    user_id = db.Column(INTEGER(unsigned=True))
    lecture_id = db.Column(INTEGER(unsigned=True))
    is_checked = db.Column(TINYINT(unsigned=True))
    created = db.Column(db.DateTime(), default=datetime.now(), index=True)


class RegisterLecture(db.Model):
    __tablename__ = 'register_lecture'

    ACCEPT = 1
    DENY = 2
    APPLYING = 4

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    student_id = db.Column(INTEGER(unsigned=True))
    lecture_id = db.Column(INTEGER(unsigned=True))
    accept_status = db.Column(TINYINT(unsigned=True))
    updated = db.Column(db.DateTime())
    created = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, student_id, lecture_id, accept_status):
        self.student_id = student_id
        self.lecture_id = lecture_id
        self.accept_status = accept_status

    @classmethod
    def check_term(cls, user_date, student_id):
        from sqlalchemy import or_

        date = user_date.split('-')
        if date[1] in Lecture.SPRING:
            return cls.query.filter(or_(cls.created.like(date[0] + '-03-%'), cls.created.like(date[0] + '-04-%')),
                                    cls.student_id == student_id).all()

        elif date[1] in Lecture.SUMMER:
            return cls.query.filter(or_(cls.created.like(date[0] + '-06-%'), cls.created.like(date[0] + '-07-%')),
                                    cls.student_id == student_id).all()

        elif date[1] in Lecture.ANTUMN:
            return cls.query.filter(or_(cls.created.like(date[0] + '-09-%'), cls.created.like(date[0] + '-10-%')),
                                    cls.student_id == student_id).all()

        elif date[1] in Lecture.WINTER:
            return cls.query.filter(or_(cls.created.like(date[0] + '-12-%'), cls.created.like(date[0] + '-01-%')),
                                    cls.student_id == student_id).all()

    def create(self):
        db.session.add(self)
        db.session.commit()
        return True
