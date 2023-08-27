#!/usr/bin/python3

from flask import Flask,render_template

app = Flask(__name__)

#routes to existing pages
@app.route('/')
def hello():
    return render_template('home.html')
@app.route('/userlogin.html')
def UserLogin():
    return render_template('userlogin.html')
@app.route('/UserSignUp.html')
def UserSignUp():
    return render_template('/UserSignUp.html')

if __name__ == "__main__":
    app.run(debug=True)
