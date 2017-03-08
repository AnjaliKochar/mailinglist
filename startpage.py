from flask import Flask,render_template
app=Flask(__name__)
@app.route('/')
def firstpage():
    return render_template('Subscribe.html')
if __name__=='__main__':
    app.run(host='127.0.0.1',port=4444,debug=True)