from flask import render_template, Blueprint, request, redirect, session, flash

from models.user import User

mod = Blueprint('website', __name__)


@mod.route('/')
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

        user = User.find_by_email_and_password(email=email, password=password)

        if not user:
            flash('잘못된 비밀번호 입니다.', 'error')
            return redirect('/login')

        session['email'] = email
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
