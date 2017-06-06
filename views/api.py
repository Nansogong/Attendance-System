from flask import Blueprint, request, jsonify, json, flash

from models.user import User
from views.decorator import login_required

mod = Blueprint('api', __name__)


@mod.route('/find_by_email', methods=['POST'])
def find_by_email():
    if request.method == 'POST':
        email = request.form.get('email')
        if User.find_by_email(email) is None:
            return jsonify(user_exist=False)
        else:
            return jsonify(user_exist=True)


@mod.route('/accept_professor', methods=['POST'])
def accept_professor():
    if request.method == 'POST':
        email = request.form.get('email')
        status = request.form.get('status')
        user = User.find_by_email(email)
        if user is None:
            flash('유저가 존재하지 않습니다', 'error')
            return jsonify(msg='user_not_exist')
        else:
            if status == 'accept':
                user.type = User.PROFESSOR_TYPE
                return jsonify(status=user.type)
            elif status == 'reject':
                user.type = User.PENDING_PROFESSOR_TYPE
                return jsonify(status=user.type)
            else:
                flash('잘못된 요청입니다', 'error')
                return jsonify(status='request_error')


@mod.route('/apply_lecture', methods=['POST'])
def apply_lecture():
    if request.method == 'POST':
        lecture_code = request.form.get('lecture_code')
        status = request.form.get('status')

        lecture = Lecture.find_by_lecture_code(lecture_code)
        user = get_current_user()
        if status == 'apply':
            register_lecture = RegisterLecture(user.id, lecture.id, RegisterLecture.APPLYING)
            register_lecture.create()
            return jsonify(status=register_lecture.accept_status)

        else:
            flash('잘못된 요청입니다', 'error')
            return jsonify(status='request_error')

