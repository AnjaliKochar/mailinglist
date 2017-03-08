from flask import Flask, render_template,redirect,url_for,request,session,flash,g
import sqlite3
import cgi,cgitb

app=Flask(__name__)
DATABASE="mailinglist.db"
app.config.from_object(__name__)

def connect_database():
    return sqlite3.connect(app.config['DATABASE'])
@app.route('/detail')
def updatepage():
    return render_template('assignnewsubmitter.html')
@app.route('/detail',methods=['get','post'])
def detail():
    g.db=connect_database()

    name=request.form['nme']
    mail=request.form['mail']
    phone=request.form['number']
    post=request.form['post']
    role=request.form['role']
    password=request.form['pswrd']
    conpswrd=request.form['conpswrd']
    subslist='none'
    mlistt=((name,mail,phone,post,role,subslist,password))
    c=g.db.execute('insert into users values(?,?,?,?,?,?,?)',mlistt)
    c=g.db.execute('select user_name,email,phoneno,company_designation,list_role,subscribed_list,password from users')
    details = [dict(user_name=row[0], email=row[1], phoneno=row[2], company_designation=row[3],list_role=row[4],subscribed_list=row[5],password=row[6]) for row in c.fetchall()]
    g.db.close()
    return render_template('login2.html', details=details)

if __name__=='__main__':
    app.run(host='127.0.0.1',port=4444,debug=True)
