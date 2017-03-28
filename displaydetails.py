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

@app.route('/subscription',methods=['get','post'])
def new_subscription():
    g.db=connect_database()
    subs_email=request.form.get('emailid')
    developer=request.form.get('developer')
    contentwriter=request.form.get('contentwriter')
    SEO=request.form.get('SEO')
    DMM=request.form.get('DMM')
    UIUX=request.form.get('UI/UX')
    GD=request.form.get('GD')
    database=request.form.get('database')
    #subscribedlist=(subs_email,developer,contentwriter,SEO,DMM,UIUX,GD,database)
    subscribedlist=[]

    listrole='Subscriber'
    if subs_email:
        c=g.db.execute('Select user_id from users where email = ?',(subs_email,))
        data=c.fetchone()
        if data is None:#cannot use try here because user's email id may be existing before but he might subscribe to new list now
            g.db.execute('Insert into users(email,list_role) values(?,?)', (subs_email, listrole,))
        c = g.db.execute('Select user_id from users where email=?', (subs_email,))#may be new record is inserted in previous query so refired this query
        userid = [dict(user_id=row[0]) for row in c.fetchall()]
        print(userid[0].get("user_id"))
        uid=userid[0].get("user_id")
        if developer:#checks if developer!=none
             c=g.db.execute('Select list_id from lists where list_name=?',('Developer',))
             listid= [dict(list_id=row[0]) for row in c.fetchall()]
             lid=listid[0].get("list_id")
             try:
                g.db.execute('Insert into subscriber_lists values (?,?)', (uid,lid))
                subscribedlist.append('Developer')
             except:
                 flash('OOPS!you are already registered to the developer list')
        if contentwriter:
             c=g.db.execute('Select list_id from lists where list_name=?',('ContentWriter',))
             listid= [dict(list_id=row[0]) for row in c.fetchall()]
             lid=listid[0].get("list_id")
             try:
                g.db.execute('Insert into subscriber_lists values (?,?)', (uid,lid))
                subscribedlist.append('Content Writer')
             except:
                 flash('OOPS!you are already registered to the Content Writer list')
        if SEO:
             c=g.db.execute('Select list_id from lists where list_name=?',('SEO',))
             listid= [dict(list_id=row[0]) for row in c.fetchall()]
             lid=listid[0].get("list_id")
             try:
                g.db.execute('Insert into subscriber_lists values (?,?)', (uid,lid))
                subscribedlist.append('SEO')
             except:
                 flash('OOPS!you are already registered to the SEO list')
        if DMM:
            c = g.db.execute('Select list_id from lists where list_name=?', ('DMM',))
            listid = [dict(list_id=row[0]) for row in c.fetchall()]
            lid = listid[0].get("list_id")
            try:
                g.db.execute('Insert into subscriber_lists values (?,?)', (uid, lid))
                subscribedlist.append('DMM')
            except:
                flash('OOPS!you are already registered to the DMM list')
        if UIUX:
             c=g.db.execute('Select list_id from lists where list_name=?',('UIUX',))
             listid= [dict(list_id=row[0]) for row in c.fetchall()]
             lid=listid[0].get("list_id")
             try:
                g.db.execute('Insert into subscriber_lists values (?,?)', (uid,lid))
                subscribedlist.append('UI/UX')
             except:
                flash('OOPS!you are already registered to the UI/UX list')
        if GD:
             c=g.db.execute('Select list_id from lists where list_name=?',('GraphicDesigner',))
             listid= [dict(list_id=row[0]) for row in c.fetchall()]
             lid=listid[0].get("list_id")
             try:
                g.db.execute('Insert into subscriber_lists values (?,?)', (uid,lid))
                subscribedlist.append('Graphic Designer')
             except:
                 flash('OOPS!you are already registered to the Graphic Designer list')
        if database:
            c = g.db.execute('Select list_id from lists where list_name=?', ('Database',))
            listid = [dict(list_id=row[0]) for row in c.fetchall()]
            lid = listid[0].get("list_id")
            try:
                g.db.execute('Insert into subscriber_lists values (?,?)', (uid, lid))
                subscribedlist.append('Database')
            except:
                flash('OOPS!you are already registered to the Database list')

        if subscribedlist:
            print(len(subscribedlist))
            msg = "Congratulations!!you are now registered to "
            lst = ",".join(subscribedlist)
            msg = msg+lst+" list"
            flash(msg)

    else:
        flash("Please enter your email id ")
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


@app.route('/curatoroptionsviewsuggestions')
def view_suggestions():
    g.db = connect_database()
    c=g.db.execute('SELECT * from submitter_suggestions')
    details=[dict(ss_id=row[0],user_id=row[1],list_id=row[2],url=row[3],title=row[4],description=row[5])for row in c.fetchall()]
    return render_template('curatorviewsuggestions.html',details=details)


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

@app.route('/submittersuggestions' , methods=['get','post'])
def submittersuggestions_method():
    g.db=connect_database()
    try:
        title=request.form.get('title')
        description=request.form.get('description')
        list_name=request.form.get('listname')
        url=request.form.get('url')
        mail = session['useremail']
        if title and description and list_name and url:
            c=g.db.execute('SELECT list_id from lists where list_name = ?',(list_name,))
            details=[dict(list_id=row[0])for row in c.fetchall()]
            lid=details[0].get("list_id")
            c=g.db.execute('SELECT user_id from users where email = ?',(mail,))
            details=[dict(user_id=row[0])for row in c.fetchall()]
            uid=details[0].get("user_id")
            c=g.db.execute('INSERT into submitter_suggestions(user_id,list_id,url,title,description)'
                           ' values(?,?,?,?,?)',(uid,lid,url ,title,description,))
            flash('Thank you for your suggestions ')
        else:
            flash('Please fill all the details')
        g.db.commit()
        g.db.close()
    except:
        flash('OOOPS!!Sorry, you cannot register the same link for the same list again')
        g.db.close()
    return render_template('submitterlinksuggest.html')

@app.route('/details')
def subdetails():
    g.db=connect_database()

    c=g.db.execute('select * from users')
    details = [dict(user_id=row[0], user_name=row[1], email=row[2], phoneno=row[3], company_designation=row[4],
                    list_role=row[5], password=row[6]) for row in c.fetchall()]
    g.db.close()
    return render_template('login2.html', details=details)



if __name__=='__main__':
    app.run(host='127.0.0.1',port=4444,debug=True)
