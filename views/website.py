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
