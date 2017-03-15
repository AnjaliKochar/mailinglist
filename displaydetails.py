from flask import Flask,g,render_template,request,flash
import sqlite3

app=Flask(__name__)
DATABASE="mailinglist.db"
app.config.from_object(__name__)
app.secret_key="key"

def connect_database():
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def firstpage():
    return render_template('Subscribe.html')

@app.route('/admin_login')
def admin_login():
     return render_template('adminlogin.html')

@app.route('/curatoroptionsassignnew')
def assign_newsubmitter():
    return render_template('assignnewsubmitter.html')

@app.route('/curatoroptionsassignnew')
def assign_newsubmittermethod():
    g.db = connect_database()

    name = request.form['nme']
    mail = request.form['mail']
    phone = request.form['number']
    post = request.form['post']
    role = request.form['role']
    password = request.form['pswrd']
    conpswrd = request.form['conpswrd']
    subslist = 'none'
    mlistt = ((name, mail, phone, post, role, subslist, password))
    c = g.db.execute('insert into users values(?,?,?,?,?,?,?)', mlistt)
    c = g.db.execute('select user_name,email,phoneno,company_designation,list_role,subscribed_list,password from users')
    g.db.commit()
    details = [dict(user_name=row[0], email=row[1], phoneno=row[2], company_designation=row[3], list_role=row[4],
                    subscribed_list=row[5], password=row[6]) for row in c.fetchall()]
    g.db.close()
    return render_template('login2.html', details=details)

@app.route('/curatoroptionsupdateprofile')
def update_profile():
    return render_template('updateprofile.html')

@app.route('/curatoroptionssendnewsletter')
def send_newsletter():
    return render_template('curatorsendnewsletter.html')

@app.route('/submitter_suggest_link')
def suggest_link():
    return render_template('submitterlinksuggest.html')

@app.route('/details')
def subdetails():
    g.db=connect_database()
    c=g.db.execute('select user_name,email,phoneno,company_designation,list_role,subscribed_list,password from users')
    details = [dict(user_name=row[0], email=row[1], phoneno=row[2], company_designation=row[3],list_role=row[4],subscribed_list=row[5],password=row[6]) for row in c.fetchall()]
    g.db.close()
    return render_template('login2.html', details=details)

@app.route('/updateddetail')
def updatepage():
    return render_template('assignnewsubmitter.html')


@app.route('/updateddetail',methods=['get','post'])
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
    g.db.commit()
    details = [dict(user_name=row[0], email=row[1], phoneno=row[2], company_designation=row[3],list_role=row[4],
                    subscribed_list=row[5],password=row[6]) for row in c.fetchall()]
    g.db.close()
    return render_template('login2.html', details=details)


@app.route('/curatororsub_login' ,methods=['get','post'])
def curatororsub_login():

    g.db = connect_database()
    profile = request.form['cors']
    aemail = request.form['adminemail']
    apswd = request.form['adminpswd']
    detaillist=((profile,aemail,apswd))
    c=g.db.execute('select * from users where list_role=? AND email=? AND password=?', detaillist)
    details = [dict(user_name=row[0], email=row[1], phoneno=row[2], company_designation=row[3], list_role=row[4],
                 subscribed_list=row[5], password=row[6]) for row in c.fetchall()]
    if len(details) > 0 and profile=='Submitter':
        g.db.close()
        return render_template('submitteroptions.html')
    elif len(details) > 0 and profile=='Curator':
        g.db.close()
        return render_template('curatoroptions.html')
    else:
        flash('sorry incorrect details !!')
        g.db.close()
        return render_template('adminlogin.html')



if __name__=='__main__':
    app.run(host='127.0.0.1',port=4444,debug=True)
