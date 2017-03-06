from flask import Flask, render_template,redirect,url_for,request,session,flash,g
from functools import wraps
import sqlite3

app=Flask(__name__)

DATABASE='mailinglist.db'
app.config.from_object(__name__)

#key is used for session encryption
app.secret_key='key'

def connect_database():
    return sqlite3.connect(app.config['DATABASE'])
def login_required(test):
    @wraps(test)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return test(*args,**kwargs)
        else:
            flash('login required !!')
            return redirect(url_for('login'))
    return wrap


@app.route('/success/<name>')
@login_required
def success(name):
    g.db=connect_database()
    c=g.db.execute('select user_name,email,phoneno,profile from users')
    #c = g.db.execute('select user_id,user_name from users')

    details=[dict(user_name=row[0],email=row[1],phoneno=row[2],profile=row[3]) for row in c.fetchall()]
    g.db.close()
    return render_template('login2.html',details=details)
    #return 'welcome %s' % name



@app.route('/')
def abc():
    return "Hi there this is home page"

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return  redirect(url_for('abc'))

@app.route('/login',methods = ['POST', 'GET'])
def login():
   error=None

   if request.method == 'POST':
       if request.form['mail'] != 'admin@lrd' and request.form['pass'] != 'admin':
           error='Invalid credentials.please try again !!'
       else:
           session['logged_in']=True
           return redirect(url_for('success',name = 'user'))
   return render_template('login1.html',error=error)


if __name__ == '__main__':
   app.run(debug = True)
