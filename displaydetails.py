from flask import Flask,g,render_template,request,flash,session
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
    return render_template('update_inputid.html')

@app.route('/curatoroptionssendnewsletter')
def send_newsletter():
    return render_template('curatorsendnewsletter.html')

@app.route('/submitter_suggest_link')
def suggest_link():
    return render_template('submitterlinksuggest.html')

@app.route('/subscription',methods=['get','postz'])
def new_subscription():
    g.db=connect_database()
    subs_email=request.form['emailid']
    developer=request.form['developer']
    contentwriter=request.form['contentwriter']
    SEO=request.form['SEO']
    DMM=request.form['DMM']
    UIUX=request.form['UI/UX']
    GD=request.form['GD']
    database=request.form['database']
    listrole='Subscriber'
    g.db.execute('Insert into users(email,list_role) values(?,?)',(subs_email,listrole,))
    g.db.execute('Insert into lists')
    g.db.commit()
    g.db.close()
    return render_template('Subscribe.html')

@app.route('/curatororsub_login' ,methods=['get','post'])
def curatororsub_login():

    g.db = connect_database()

    profile = request.form['cors']
    aemail = request.form['adminemail']
    apswd = request.form['adminpswd']
    detaillist=((profile,aemail,apswd))
    c=g.db.execute('select user_name from users where list_role=? AND email=? AND password=?', detaillist)
    details = [dict(user_name=row[0]) for row in c.fetchall()]
    session['useremail'] = aemail
    if len(details) > 0 and profile=='Submitter':
        g.db.close()
        return render_template('submitteroptions.html')
    elif len(details) > 0 and profile=='Curator':
        g.db.close()
        return render_template('curatoroptions.html',session=session)
    else:
        flash('sorry incorrect details !!')
        session.pop('useremail')
        g.db.close()
        return render_template('adminlogin.html')




@app.route('/curatoroptionsassignnew',methods=['get','post'])
def assign_newsubmittermethod():
    g.db = connect_database()
    mail = request.form['email'] #cannot use session because updation of another id is done
    c=g.db.execute('select user_name,list_role from users where email=?',(mail,))
    details=[dict(name=row[0],listrole=row[1],email=mail) for row in c.fetchall()]
    g.db.close()
    return render_template('newsubmitterdisplay.html', details=details)

@app.route('/updatesubmitterbycurator',methods=['get','post'])
def updatesubmitter_curator():
    g.db=connect_database()
    mail = request.form['mail']
    role = request.form['role']
    c = g.db.execute('update users set list_role=? where email=?', (role,mail,))
    g.db.commit()
    # c = g.db.execute('select * from users')
    # details = [dict(user_id=row[0],user_name=row[1],email=row[2], phoneno=row[2], company_designation=row[3], list_role=row[4],
    #                 password=row[5]) for row in c.fetchall()]
    g.db.close()
    flash('RECORDS UPDATED !!')
    return render_template('curatoroptions.html')


@app.route('/curatoroptionsupdateprofile',methods=['get','post'])
def detail():
    g.db=connect_database()
    mail=session['useremail']

    c=g.db.execute('Select * from users where email=?',(mail,))
    details = [dict(user_id=row[0], user_name=row[1], email=row[2], phoneno=row[3], company_designation=row[4],
                    list_role=row[5],
                    password=row[6]) for row in c.fetchall()]
    g.db.close()

    return render_template('updateprofile.html', details=details)


@app.route('/curatoroptionsprofileupdateclick',methods=['get','post'])
def curatorupdateprofile_submitclick():
    g.db=connect_database()
    userid=request.form['userid']
    name=request.form['name']
    email=request.form['email']
    contact=request.form['contactnumber']
    designation=request.form['designation']
    listrole=request.form['listrole']
    password=request.form['password']

    updatelist=(name,email,contact,designation,listrole,password,userid)
    c=g.db.execute('UPDATE users set user_name=?,email=?,phoneno=?,company_designation=?,list_role=?,password=? where user_id=?',updatelist)
    g.db.commit()
    # c = g.db.execute('select * from users')
    # details = [dict(user_id=row[0], user_name=row[1], email=row[2], phoneno=row[2], company_designation=row[3],
    #                 list_role=row[4],
    #                 password=row[5]) for row in c.fetchall()]
    g.db.close()
    flash('RECORDS UPDATED !!')
    return render_template('curatoroptions.html')


@app.route('/details')
def subdetails():
    g.db=connect_database()

    c=g.db.execute('select user_name,email,phoneno,company_designation,list_role,subscribed_list,password from users')
    details = [dict(user_name=row[0], email=row[1], phoneno=row[2], company_designation=row[3],list_role=row[4],subscribed_list=row[5],password=row[6]) for row in c.fetchall()]
    g.db.close()
    return render_template('login2.html', details=details)



if __name__=='__main__':
    app.run(host='127.0.0.1',port=4444,debug=True)
