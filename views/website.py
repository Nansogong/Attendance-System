from flask import render_template, Blueprint, request, redirect, session

from models.user import User

mod = Blueprint('website', __name__)


@mod.route('/')
def home():
    return render_template('index.html', title='Nansogong')


@mod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title='Login')
    elif request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        User.find_by_email(email)

        session['email'] = email
        return redirect('/')
