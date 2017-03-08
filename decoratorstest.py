# from flask import Flask
# app=Flask(__name__)
#
# def decorator(test):
#     return "this is decorator"
#
# @app.route('/')
# @decorator
# def func():
#     pass
#
# if __name__ == '__main__':
#    app.run(debug = True)

from flask import Flask
from functools import wraps
app=Flask(__name__)

@app.route('/hello')
def hy():
    return  "this is decorator"
def decorator(test):
    @wraps(test)
    def abc(*args,**kwargs):
       print( "this is decorator")
       return test(*args,**kwargs)
    return abc

@app.route('/')
@decorator
def func():
    return "This is func !!"

if __name__ == '__main__':
   app.run(host='127.0.0.1',port=4444,debug = True)