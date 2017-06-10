from functools import reduce

import datetime
from flask import render_template, Blueprint, request, redirect, session, flash

from models.user import User
from models.lecture import Lecture, LectureDay, RegisterLecture

from views.decorator import login_required

mod = Blueprint('website', __name__)

admin_id = 'nansogong'
admin_password = 'sksthrhd'


@mod.route('/')
@login_required
def home():
    return render_template('index.html', title='Nansogong')


@mod.route('/admin', methods=['GET'])
def admin():
    if request.method == 'GET':
        return render_template('admin.html', title='Admin')


@mod.route('/accept_professor_lecture', methods=['GET'])
def accept_professor():
    if request.method == 'GET':
        return render_template('accept_professor_lecture.html', title='Accept_professor')


@mod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # TODO: 클라이언트에서 아래의 flashing보고 작업해야함. 예를들면 아래 잘못된 비밀번호 출력
        # TODO: http://ned.im/noty/options.html 을 base.html 에 넣는 것을 추천함. 만약 JS를 쓴다면 test code를 짜야할 것
        # http://flask.pocoo.org/docs/0.12/patterns/flashing/#flashing-with-categories
        return render_template('login.html', title='Login')
    elif request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        if email == 'nansogong' and password == 'sksthrhd':
            session['email'] = 'admin'
            return redirect('/admin')

        user = User.find_by_email_and_password(email=email, password=password)

        if not user:
            flash('잘못된 비밀번호 입니다.', 'error')
            return redirect('/login')

        session['email'] = email
        return redirect('/')


@mod.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')


@mod.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', title='회원가입')
    elif request.method == 'POST':
        user_num = request.form.get('user_num', None)
        name = request.form.get('name', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        fingerprint = request.form.get('fingerprint', None)
        type = request.form.get('type', None)
        if type == str(User.PROFESSOR_TYPE):
            type = User.PENDING_PROFESSOR_TYPE
        if user_num is None or name == '' or email == '' or password == '' or fingerprint == '' or type is None:
            flash('작성되지 않은 필드가 있습니다.', 'error')
            return redirect('/register')
        elif User.find_by_email(email):
            flash('이미 가입된 이메일입니다.', 'error')
            return redirect('/register')
        elif User.find_by_user_num(user_num):
            flash('이미 가입된 학번입니다 ㅠㅠ', 'error')
            return redirect('/register')

        user = User(user_num=user_num, name=name, email=email, password=password, fingerprint=fingerprint, type=type)
        user.create()

        return redirect('/login')


@mod.route('/lectures', methods=['GET'])
@login_required
def lecture_list():
    user = get_current_user()

    lectures = dict()
    user_date = str(datetime.datetime.now())

    if user.type & User.PROFESSOR_TYPE:
        lectures['professor'] = Lecture.get_my_current_lecture(user_date, user.id)

    if user.type & User.STUDENT_TYPE:
        lectures['student'] = RegisterLecture.check_term(user_date, user.id)

    return render_template('lectures.html', lectures=lectures)


@mod.route('/lectures/create', methods=['GET', 'POST'])
@login_required
def create_lecture():
    user = check_user_permission(User.PROFESSOR_TYPE)

    if not user:
        return render_template('forbidden.html'), 403
    if request.method == 'GET':
        return render_template('create_lecture.html', title='Create Lecture')
    elif request.method == 'POST':
        import datetime

        name = request.form.get('name', None)
        lecture_code = request.form.get('lecture_code', None)
        criteria_of_F = request.form.get('criteria_of_F', None)
        start1 = request.form.get('start1', None)
        time1 = request.form.get('time1', None)
        day1 = request.form.get('day1', None)
        start2 = request.form.get('start2', None)
        time2 = request.form.get('time2', None)
        day2 = request.form.get('day2', None)

        if name == '' or lecture_code is None or start1 == '' or time1 is None or day1 is None:
            flash('작성되지 않은 필드가 있습니다.', 'error')
            return redirect('/lectures/create')

        if start2 != "" or time2 is not None or day2 is not None:
            if time2 is None or day2 is None or start2 == "":
                flash('작성되지 않은 필드가 있습니다.', 'error')
                return redirect('/lectures/create')

        if Lecture.check_term(str(datetime.datetime.now()), lecture_code):
            flash('이미 생성된 강의번호입니다.', 'error')
            return redirect('/lectures/create')

        lecture = Lecture(professor_id=user.id, name=name, lecture_code=lecture_code,
                          criteria_of_F=criteria_of_F)

        lecture.create()

        lecture_day = LectureDay(start=start1, time=time1, day=day1, lecture_id=lecture.id)

        lecture_day.create()

        if start2 != "":
            lecture_day = LectureDay(start=start2, time=time2, day=day2, lecture_id=lecture.id)

            lecture_day.create()

        return redirect('/lectures')


@mod.route('/lectures/search_lecture', methods=['GET'])
@login_required
def search_lecture():
    user = check_user_permission(User.STUDENT_TYPE)

    if not user:
        return render_template('forbidden.html'), 403
    if request.method == 'GET':
        lectures = Lecture.get_current_semester()
        return render_template('search_lecture.html', lectures=lectures)


@mod.route('/lectures/accept_student', methods=['GET'])
@login_required
def accept_student():
    user = check_user_permission(User.PROFESSOR_TYPE)

    if not user:
        return render_template('forbidden.html'), 403
    if request.method == 'GET':
        user = get_current_user()
        register_lectures = RegisterLecture.get_current_semester_professor(user.id)
        return render_template('accept_student.html', register_lectures=register_lectures)


@mod.route('/professor_list', methods=['GET'])
@login_required
def professor_list():
    user = check_user_permission(User.PROFESSOR_TYPE)

    if not user:
        return render_template('forbidden.html'), 403
    if request.method == 'GET':
        """
        professor, accepted professor type순으로 리스트 설정
        """
        professors = User.get_all_filter_by_type(User.PROFESSOR_TYPE) + \
                     User.get_all_filter_by_type(User.PENDING_PROFESSOR_TYPE)
        return render_template('accept_professor.html', professors=professors)


def check_user_permission(required_type):
    """
    requried_type 에는 퍼미션이 들어옵니다 퍼미션은 Models.user에 있는 User Class에 있습니다
    User.PROFESSOR_TYPE 이 예입니다.
    퍼미션이 여러개가 들어와도 됩니다. 그때는 리스트로 보내주면 됩니다.
    ex. required_type = [ professor_type, ta_type ]

    만약 권한이 없다면 403 (forbidden)이 status code 로 리턴됩니다.
    """
    if type(required_type) == list:
        required_type = reduce(lambda x, y: x | y, required_type)

    email = session.get('email', None)
    user = User.find_by_email(email)

    if not user or not (user.type & required_type):
        flash('권한이 없습니다')
        return None

    return user


def get_current_user():
    email = session.get('email', None)
    return User.find_by_email(email)
