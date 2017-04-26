from functools import wraps
from flask import session,flash,render_template
def login_required(test):
    @wraps(test)
    def wrap(*args,**kwargs):
        if session['logged_in'] == True :
            print('i m not clearing session')
            return test(*args,**kwargs)
        else:

            flash('login required !!')
            return render_template('Subscribe.html')
    return wrap