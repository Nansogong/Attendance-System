from functools import reduce

from flask import render_template, Blueprint, request, redirect, session, flash

from models.user import User
from models.lecture import Lecture, LectureDay
from views.decorator import login_required

mod = Blueprint('website', __name__)


@mod.route('/')
@login_required
def home():
    return render_template('index.html', title='Nansogong')


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
        return render_template('register.html', title='Register')
    elif request.method == 'POST':
        user_num = request.form.get('user_num', None)
        name = request.form.get('name', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        fingerprint = request.form.get('fingerprint', None)
        type = request.form.get('type', None)

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


@mod.route('/lectures', methods=['GET', 'POST'])
@login_required
def lecture_list():
    return render_template('lectures.html')


@mod.route('/lectures/create', methods=['GET', 'POST'])
@login_required
def create_lecture():
    user = check_user_permission(User.PROFESSOR_TYPE)

    if not user:
        return render_template('forbidden.html'), 403
    if request.method == 'GET':
        return render_template('create_lecture.html', title='Create Lecture')
    elif request.method == 'POST':
        name = request.form.get('name', None)
        lecture_code = request.form.get('lecture_code', None)
        criteria_of_F = request.form.get('criteria_of_F', None)
        start = request.form.get('start', None)
        time = request.form.get('time', None)
        day = request.form.get('day', None)

        if name == '' or lecture_code is None or start == '' or time is None or day is None:
            flash('작성되지 않은 필드가 있습니다.', 'error')
            return redirect('/lectures/create')

        lecture = Lecture(professor_id=user.id, name=name, lecture_code=lecture_code,
                          criteria_of_F=criteria_of_F)

        lecture.create()

        lecture_day = LectureDay(start=start, time=time, day=day, lecture_id=lecture.id)

        lecture_day.create()
        
        return redirect('/lectures')


def check_user_permission(required_type):
    """
    requried_type 에는 퍼미션이 들어옵니다 퍼미션은 Models.user에 있는 User Class에 있습니다
    User.PROFESSOR_TYPE 이 예입니다.
    퍼미션이 여러개가 들어돠도 됩니다. 그때는 리스트로 보내주면 됩니다.
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
