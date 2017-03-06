from flask import Flask,g,render_template
import sqlite3

app=Flask(__name__)
DATABASE="mailinglist.db"
app.config.from_object(__name__)

def connect_database():
    return sqlite3.connect(app.config['DATABASE'])
@app.route('/details')
def subdetails():
    g.db=connect_database()
    c=g.db.execute('select user_name,email,phoneno,company_designation,list_role,subscribed_list,password from users')
    details = [dict(user_name=row[0], email=row[1], phoneno=row[2], company_designation=row[3],list_role=row[4],subscribed_list=row[5],password=row[6]) for row in c.fetchall()]
    g.db.close()
    return render_template('login2.html', details=details)

if __name__=='__main__':
    app.run(debug=True)
