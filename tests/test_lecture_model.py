import pytest


def test_create_lecture_day():
    from models.lecture import LectureDay
    lecture_day = LectureDay(start="10:30", time=2, day=LectureDay.MON)
    lecture_day.create()
    assert lecture_day.id > 0


def test_create_lecture(user):
    from models.lecture import Lecture
    lecture = Lecture(professor_id=user.id, name="sogong", lecture_code="asdffda", lecture_day_id=1)
    lecture.create()
    assert lecture.id > 0
