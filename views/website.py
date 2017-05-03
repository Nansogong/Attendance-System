from flask import render_template, Blueprint

mod = Blueprint('website', __name__)


@mod.route('/')
def home():
    return render_template('index.html', title='Nansogong')
