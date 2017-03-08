from flask import Flask,render_template

app=Flask(__name__)


@app.route('/')
def firstpage():
    return render_template('Subscribe.html')

@app.route('/admin_login')
def admin_login():
     return render_template('adminlogin.html')

if __name__=='__main__':
    app.run(host='127.0.0.1',port=4444,debug=True)