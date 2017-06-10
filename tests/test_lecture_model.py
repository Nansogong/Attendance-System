import pytest
import sys


def test_create_lecture(login_user):
    from flask import session
    from models.lecture import Lecture

    lecture = Lecture(professor_id=login_user.id, name="sogong", lecture_code="asdffda")
    lecture.create()
    assert lecture.id > 0


def test_create_lecture_day(lecture):
    from models.lecture import LectureDay
    lecture_day = LectureDay(start="10:30", time=2, day=LectureDay.MON, lecture_id=lecture.id)
    lecture_day.create()
    assert lecture_day.id > 0


def test_create_RegisterLecture_success(lecture):
    from models.lecture import RegisterLecture

    register_lecture = RegisterLecture(student_id=lecture.professor_id, lecture_id=lecture.id,
                                       accept_status=RegisterLecture.APPLYING)
    register_lecture.create()
    assert register_lecture.id > 0


def test_find_by_lecture_code():
    from models.lecture import Lecture
    lecture_code = 12364
    lecture = Lecture.find_by_lecture_code(lecture_code=lecture_code)

    assert lecture.lecture_code == '12364'


def test_find_register_lecture_by_student_id_lecture_id():
    from models.lecture import RegisterLecture, Lecture
    from models.user import User

    student_num = 2010036113
    lecture_code = 12364

    user = User.find_by_user_num(student_num)
    lecture = Lecture.find_by_lecture_code(lecture_code)
    register_lecture = RegisterLecture.find_register_lecture_by_student_id_lecture_id(user.id, lecture.id)

    assert register_lecture.student_id == user.id
    assert register_lecture.lecture_id == lecture.id
