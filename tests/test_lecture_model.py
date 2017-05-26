import pytest
import sys

if sys.version_info >= (3, 6):
    try:
        from app import app  # 지우지 말 것
    except ModuleNotFoundError as e:
        import os
        myPath = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, myPath + '/../')
        from app import app
else:
    try:
        from app import app  # 지우지 말 것
    except ImportError as e:
        import os
        myPath = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, myPath + '/../')
        from app import app


def test_create_lecture_day():
    from models.lecture import LectureDay
    lecture_day = LectureDay(start="10:30", time=2, day=LectureDay.MON)
    lecture_day.create()
    assert lecture_day.id > 0


def test_create_lecture(create_user_first):
    from models.lecture import Lecture
    lecture = Lecture(professor_id=create_user_first.id, name="sogong", lecture_code="asdffda", lecture_day_id=1)
    lecture.create()
    assert lecture.id > 0