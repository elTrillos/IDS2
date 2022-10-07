from datetime import datetime
from unicodedata import category
from xmlrpc.client import DateTime

from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)
app.app_context().push()

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

class Emprendimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(80))
    descripcion = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Emprendimiento %r>' % self.name

class Puntuacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    id_emprendimiento = db.Column(db.Integer, nullable=False)
    puntos = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<Puntuacion %r>' % self.name

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    disponibilidad = db.Column(db.Integer)
    precio = db.Column(db.String(80))
    id_emprendimiento = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<Producto %r>' % self.name

class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80))
    id_producto = db.Column(db.Integer, nullable=False)
    id_user = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<Producto %r>' % self.name

@app.route('/', methods=['GET','POST']) # login
def index():
    if request.method == "POST":
        uname = request.form["username"]
        passw = request.form["password"]
        login = User.query.filter_by(username=uname, password=passw).first()
        #session['username'] = uname
        #session['taskTodo'] = login.current_todo
        #session['taskStep'] = login.current_step
        #session['user_id'] = login.id
        print(login)
        if login is not None:
            #if login.category=='teacher':
            #    return redirect(url_for("index"))
            #else:
            print("llendo al index")
            return redirect('/index')
    return render_template('login.html')

@app.route('/emprendimientos' , methods=['POST','GET'])
def emprendimientos():
    emprendimientos=Emprendimiento.query.order_by(Emprendimiento.id).all()
    return render_template('emprendimientos.html',emprendimientos=emprendimientos)

@app.route('/misEmprendimientos' , methods=['POST','GET'])
def misEmprendimientos():
    misEmprendimientos=Emprendimiento.query.order_by(Emprendimiento.id).all() #Falta hacer el query que revise si son los emps del usuario y me da paja hacerlo ahora
    return render_template('mis_emprendimientos.html',emprendimientos=misEmprendimientos)


@app.route('/emprendimiento/<int:id>' , methods=['POST','GET'])
def emprendimiento(id):
    currentEmprendimiento=Emprendimiento.query.get_or_404(id)
    return render_template('emprendimiento.html',emprendimiento=currentEmprendimiento) #hagan las views porfa 





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
        print(login)
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
        cat = request.form['category']
        numb = request.form['phone']
        rname = request.form['name']
        register = User(username = uname, email = mail, password = passw, category=cat, telefono=numb, nombre=rname)
        db.session.add(register)
        #session["user"] = register
        db.session.commit()
        return redirect(url_for("login"))    
    return render_template("register.html")

@app.route("/index", methods=["GET", "POST"])
def indexIn():
    return render_template("index.html")
if __name__ =="__main__":
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run()