from functools import wraps
from flask import flash, redirect, session


# Login required decorator.
def login_required(method):
    @wraps(method)
    def wrap(*args, **kwargs):
        if 'email' in session:
            return method(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect('/login')
    return wrap
