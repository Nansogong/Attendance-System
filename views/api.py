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


def json_list(list):
    lst = []
    for professor in list:
        d = {'user_num': professor.user_num, 'name': professor.name, 'email': professor.email, 'status': professor.type}
        lst.append(d)
    json.dumps(lst)
    f = {'list': lst}
    return json.dumps(f)


@mod.route('/professor_list', methods=['GET'])
def professor_list():
    if request.method == 'GET':
        """ professor, accepted_professor 순  -> sort를 통해 생성된 순서로 정렬하고싶지만 하면 효율이 떨어질 것 같다. """
        professors = User.get_all_filter_by_type(User.PROFESSOR_TYPE) + \
                     User.get_all_filter_by_type(User.ACCEPTED_PROFESSOR_TYPE) + \
                     User.get_all_filter_by_type(User.REJECTED_PROFESSOR_TYPE)
        return json_list(professors)


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
                user.type = User.ACCEPTED_PROFESSOR_TYPE
                return jsonify(status=user.type)
            elif status == 'reject':
                user.type = User.REJECTED_PROFESSOR_TYPE
                return jsonify(status=user.type)
            elif status == 'cancel':
                user.type = User.PROFESSOR_TYPE
                return jsonify(status=user.type)
            else:
                flash('잘못된 요청입니다', 'error')
                return jsonify(status='request_error')
