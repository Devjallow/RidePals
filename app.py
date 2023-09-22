#!/usr/bin/python3

from flask import Flask,render_template,flash,logging, url_for, request, redirect, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import bcrypt
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'the random string'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self,name,lastname,email,password):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))
with app.app_context():
        db.create_all()


# routes to existing pages
@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/UserSignUp', methods=['POST','GET'])
def UserSignUp():
    
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name,lastname=lastname,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('You have succesfullly Register')
        return redirect('Userlogin')  # This line should not be indented
    return render_template('UserSignUp.html')

#Admin email is Admin@admin.com password = password
@app.route('/Userlogin', methods=['GET','POST'])
def userLogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/AdminDashbord')
        else:
            return render_template('Userlogin.html')

    return render_template('Userlogin.html')
@app.route('/AdminDashbord')
def dashboard():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('AdminDashbord.html',user=user)    

    return redirect('/Userlogin.html')  


if __name__ == "__main__":
    app.run(debug=True)
