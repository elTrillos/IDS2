from unicodedata import category
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))
    category = db.Column(db.String(80), nullable=False)
    telefono = db.Column(db.String(80))
    nombre = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/', methods=['POST','GET'])
def index():
        return render_template('index.html')

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["username"]
        passw = request.form["password"]
        login = User.query.filter_by(username=uname, password=passw).first()
        session['username'] = uname
        session['taskTodo'] = login.current_todo
        session['taskStep'] = login.current_step
        session['user_id'] = login.id
        if login is not None:
            if login.category=='teacher':
                return redirect(url_for("index"))
            else:
                print("xdddasdeasd")
                current_user_category = User.query.get_or_404(session['user_id']).category
                return render_template('index.html')
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['username']
        mail = request.form['email']
        passw = request.form['password']
        register = User(username = uname, email = mail, password = passw)
        db.session.add(register)
        #session["user"] = register
        db.session.commit()
        return redirect(url_for("login"))    
    return render_template("register.html")

if __name__ =="__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()