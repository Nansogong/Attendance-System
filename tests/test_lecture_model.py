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