from datetime import datetime
import re

from unicodedata import category
from xmlrpc.client import DateTime

from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

#Nombre de la base de datos
DB_NAME = "test.db"

app = Flask(__name__)
TEMP_PATH = './static/temp'
UPLOAD_FOLDER = './static/upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    emprendimiento = relationship("Emprendimiento", back_populates="user")
    def __repr__(self):
        return "<User(username='%s',category='%s',telefono='%s',nombre='%s',email='%s')>" % (
            self.username,
            self.category,
            self.telefono,
            self.nombre,
            self.email
            )

class Emprendimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="emprendimiento")
    nombre = db.Column(db.String(80))
    categoria = db.Column(db.String(80), nullable=True)
    descripcion = db.Column(db.String(80), nullable=False)
    imagen_name=db.Column(db.String(80), nullable=True)
    productos = db.relationship('Producto', backref='emprendimiento', lazy=True)
    imagenes = db.relationship('EmprendimientoImage', backref='emprendimiento', lazy=True)
    puntuaciones = db.relationship('Puntuacion', backref='emprendimiento', lazy=True)
    def __repr__(self):
        return '<Emprendimiento %r>' % self.id


class EmprendimientoImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagename = db.Column(db.Text(), nullable = True)
    id_emprendimiento = db.Column(db.Integer, db.ForeignKey('emprendimiento.id'), nullable=False)
    def __repr__(self):
        return '<EmprendimientoImage %r>' % self.id

class Puntuacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_emprendimiento = db.Column(db.Integer, db.ForeignKey('emprendimiento.id'), nullable=False)
    puntos = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<Puntuacion %r>' % self.id

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    descripcion = db.Column(db.Text)
    disponibilidad = db.Column(db.Integer)
    imagen_name=db.Column(db.String(80), nullable=True)
    precio = db.Column(db.String(80))
    id_emprendimiento = db.Column(db.Integer, db.ForeignKey('emprendimiento.id'), nullable=False)
    imagenes = db.relationship('ProductImage', backref='producto', lazy=True)
    opiniones= db.relationship('Opinion', backref='producto', lazy=True)
    fecha = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<Producto %r>' % self.id

class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagename = db.Column(db.Text(), nullable = True)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    def __repr__(self):
        return '<ProductoImage %r>' % self.id

class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text())
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<Producto %r>' % self.id
    
if not os.path.exists('instance/' + DB_NAME):
    with app.app_context():
            db.create_all()
            print("Database Created")

@app.route('/', methods=['GET','POST']) # login
def index():
    if not session.get('user_id'):
        return redirect(url_for("login"))  
    else:
        allProductos=Producto.query.order_by(Producto.id).all()
        allEmprendimientos=Emprendimiento.query.order_by(Emprendimiento.id).all()
        producto_emprendimiento_id=db.session.query(Emprendimiento).filter(Emprendimiento.id_usuario==session.get('user_id')).first()
        return render_template('index.html', productos=allProductos, emprendimientos=allEmprendimientos, misEmps=producto_emprendimiento_id)

@app.route('/emprendimientos' , methods=['POST','GET'])
def emprendimientos():
    if not session.get('user_id'):
        return redirect(url_for("login"))
    else:    
        emprendimientos=Emprendimiento.query.order_by(Emprendimiento.id).all()
        return render_template('emprendimientos.html',emprendimientos=emprendimientos)

@app.route('/nuevoEmprendimiento', methods=['POST','GET'])
def nuevoEmprendimiento():
    if not session.get('user_id'):
        return redirect(url_for("login"))
    else:
        if request.method == 'POST':
            emprendimiento_nombre=request.form['nombre']
            emprendimiento_descripcion = request.form['descripcion']
            emprendimiento_categoria = request.form['categoria']
            user_id=User.query.get_or_404(session['user_id']).id
            print("xd")
            try:
                print("xd")
                file = request.files['photo']
                image_name=os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                filename = secure_filename(file.filename)
                image_name=image_name.replace('./static/upload/','')
                newEmp = Emprendimiento(descripcion = emprendimiento_descripcion,id_usuario=user_id, nombre=emprendimiento_nombre, categoria=emprendimiento_categoria, imagen_name=image_name)
                #newImage=EmprendimientoImage(id_emprendimiento=newEmp.id, imagename=image_name)
                print("xd")
                try:
                    db.session.add(newEmp)
                    #db.session.add(newImage)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    db.session.commit()
                    return redirect('/')
                except:
                    print("xd")
                    return 'Xd fallo la wea'
            except:
                print("xd")
                newEmp = Emprendimiento(descripcion = emprendimiento_descripcion,id_usuario=user_id, nombre=emprendimiento_nombre, categoria=emprendimiento_categoria)
                try:
                    db.session.add(newEmp)
                    db.session.commit()
                    return redirect('/')
                except:
                    print("xd")
                    return 'Xd fallo la wea'


        else:
            return render_template('crear_emprendimiento.html')


@app.route('/misEmprendimientos' , methods=['POST','GET'])
def misEmprendimientos():
    if not session.get('user_id'):
        return redirect(url_for("login"))
    else:
        misEmprendimientos=Emprendimiento.query.order_by(Emprendimiento.id).all() #Falta hacer el query que revise si son los emps del usuario y me da paja hacerlo ahora
        return render_template('mis_emprendimientos.html',emprendimientos=misEmprendimientos)


@app.route('/emprendimiento/<int:id>' , methods=['POST','GET'])
def emprendimiento(id):
    if not session.get('user_id'):
        return redirect(url_for("login"))
    else:
        currentEmprendimiento=Emprendimiento.query.get_or_404(id)
        
        imagenesEmp=db.session.query(EmprendimientoImage).join(Emprendimiento).filter(EmprendimientoImage.id_emprendimiento==id).all()
        productosEmp=db.session.query(Producto).join(Emprendimiento).filter(Producto.id_emprendimiento==currentEmprendimiento.id).all()
        user_id=User.query.get_or_404(session['user_id']).id
        #promedio = db.session.query(Puntuacion).where(id_emprendimiento = currentEmprendimiento.id).avg(puntos)
        if request.method == 'POST':
            
            puntos = request.form['puntaje']
            newPts = Puntuacion(id_usuario = user_id, id_emprendimiento = currentEmprendimiento.id, puntos = puntos)
           
            try:
                    db.session.add(newPts)
                    db.session.commit()
                    return redirect('/')
            except:
                print("xd")
                return 'Xd fallo la wea'
        
        return render_template('emprendimiento.html',emprendimiento=currentEmprendimiento, productos=productosEmp, imagenes=imagenesEmp ,userId=user_id) #hagan las views porfa 

## EDITAR EMPRENDIMIENTOS
@app.route('/emprendimiento/edit/<int:id>', methods=['GET', 'POST'])
def edit_emprendimiento(id):
    
    currentEmpre = Emprendimiento.query.get_or_404(id)
    
    if currentEmpre:
        if request.method == 'POST':
            currentEmpre.nombre = request.form['nombre']
            currentEmpre.descripcion = request.form['descripcion']
            currentEmpre.categoria = request.form['categoria']
            
            # save edits
            db.session.add(currentEmpre)
            db.session.commit()
            flash('emprendimiento updated successfully!')
            
            return redirect(url_for('emprendimiento', id=currentEmpre.id))
        
        return render_template('editar_emprendimiento.html', emprendimiento = currentEmpre)
    else:
        return 'Error loading #{id}'.format(id=id)

@app.route('/producto/<int:id>', methods=['POST','GET'])
def producto(id):
    if not session.get('user_id'):
        return redirect(url_for("login"))
    else:
        currentDatetime = datetime.now()
        currentProducto=Producto.query.get_or_404(id)
        imagenesProd=db.session.query(ProductImage).join(Producto).filter(ProductImage.id_producto==id).all()
        return render_template('producto.html',producto=currentProducto,imagenes=imagenesProd, currentdate=currentDatetime) #hagan las views porfa

@app.route('/nuevoProducto', methods=['POST','GET'])
def nuevoProducto():
    if not session.get('user_id'):
        return redirect(url_for("login"))
    else:
        if request.method == 'POST':
            print("deberiaPrintear")
            user_id=User.query.get_or_404(session['user_id']).id
            print("deberiaPrintear1")
            #print(request.form['nombre'])
            producto_descripcion = request.form['descripcion']
            print("deberiaPrintear3")
            producto_disponibilidad = request.form['disponibilidad']
            print("deberiaPrintear4")
            producto_nombre=request.form['nombre']
            print("deberiaPrintear2")
            producto_precio = int(request.form['precio'])
            print("deberiaPrintear5")
            #producto_fecha= datetime.now
            print("debug1")
            print(user_id)
            print("debug1")
            producto_emprendimiento_id=db.session.query(Emprendimiento).filter(Emprendimiento.id_usuario==user_id).first().id
            print("debug1")
            user_id=User.query.get_or_404(session['user_id']).id
            try:
                #print("debug1")
                file = request.files['photo']
                print("debug2")
                image_name=os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                print("debug3")
                filename = secure_filename(file.filename)
                print("debug4")
                image_name=image_name.replace('./static/upload/','')
                print("debug5")
                newProd = Producto(descripcion = producto_descripcion,id_emprendimiento=producto_emprendimiento_id, nombre=producto_nombre,disponibilidad=producto_disponibilidad,precio=producto_precio, imagen_name=image_name)
                try:
                    db.session.add(newProd)
                    #db.session.add(newImage)
                    print("debug6")
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    print("debug7")
                    db.session.commit()
                    return redirect('/')
                except:
                    return 'Xd fallo la wea'
            except:
                print("aaaa")
                newProd = Producto(descripcion = producto_descripcion,id_emprendimiento=producto_emprendimiento_id, nombre=producto_nombre,disponibilidad=producto_disponibilidad,precio=producto_precio)
                try:
                    db.session.add(newProd)
                    db.session.commit()
                    print(misProductos=Producto.query.order_by(Producto.id).all())
                    return redirect('/')
                except:
                    return 'Xd fallo la wea'

        else:
            print(session['user_id'])
            return render_template('crear_producto.html')


@app.route('/editProducto/<id>', methods=['PUT'])
def editProducto(id):
    if not session.get('user_id'):
        return redirect(url_for("login"))
    else:
        if request.method == 'PUT':
            try:
                producto = Producto.query.get_or_404(id)
                producto.descripcion = request.form['descripcion']
                producto.disponibilidad = request.form['disponibilidad']
                producto.nombre = request.form['nombre']
                producto.precio = int(request.form['precio'])
                db.session.commit()
                flash('Product updated successfully!')
                return redirect(url_for("index"))
            except:
                flash('Failed to update product')
                return 'error'

 
@app.route("/perfil/<int:id>",methods=["GET", "POST"])
def perfil(id):
    if not session.get('user_id'):
        return redirect(url_for("login"))
    else:   
        currentProfile=User.query.get_or_404(id) #current_user = User.query.get_or_404(session['user_id'])
        return render_template('profile.html',profile=currentProfile) #hagan las views porfa 

@app.route("/miPerfil",methods=["GET", "POST"])
def miPerfil():
    if not session.get('user_id'):
        return redirect(url_for("login"))
    else:
        current_user = User.query.get_or_404(session['user_id'])
        return render_template('profile.html',profile=current_user) #hagan las views porfa 

## CREAR COMENTARIO
@app.route('/comentario', methods=['POST','GET'])
def nuevaOpinion():
    if not session.get('user_id'):
        return redirect(url_for("login"))
    else:
        if request.method == 'POST':
            descripcion = request.form['descripcion']
            producto = request.form['producto_id']
            

            newOpinion = Opinion(descripcion = descripcion ,id_producto = producto,id_user = user_id)

            try:
                db.session.add(newOpinion)
                db.session.commit()
                flash('Comentado!!')

                return redirect('/')
            
            except:
                return 'Xd fallo la wea'
            
        else:
            return render_template('emprendimiento.html') #Crear VIEW PARA CREAR COMENTARIO

## Obtener promedio de puntuacion de un emprendimiento
@app.route('/puntuacion/<int:id>', methods=['POST','GET'])
def promedioPuntuacion(id):
    if not session.get('user_id'):
        return redirect(url_for("login"))
    else:
        
        user_id = User.query.get_or_404(session['user_id']).id
        emprendimiento=Emprendimiento.query.get_or_404(id)
        imagenesEmp=db.session.query(EmprendimientoImage).join(Emprendimiento).filter(EmprendimientoImage.id_emprendimiento==id).all()
        productosEmp=db.session.query(Producto).join(Emprendimiento).filter(Producto.id_emprendimiento==emprendimiento.id).all()
        
        if emprendimiento is not None:
            puntuacion = Puntuacion.query.filter_by(id_emprendimiento=emprendimiento.id).all()
            if puntuacion:
                print(puntuacion)
                promedio = 0
                for i in puntuacion:
                    promedio = i.puntos
                promedio = int(promedio/int(len(puntuacion)))
                return render_template('emprendimiento.html',emprendimiento=emprendimiento, productos=productosEmp, imagenes=imagenesEmp ,userId=user_id, puntuacion=promedio) #DEFINIR VIEW
            else:
                return render_template('emprendimiento.html',emprendimiento=emprendimiento, productos=productosEmp, imagenes=imagenesEmp ,userId=user_id) #DEFINIR VIEW
        return render_template('emprendimiento.html',emprendimiento=emprendimiento, productos=productosEmp, imagenes=imagenesEmp ,userId=user_id) #DEFINIR VIEW
    
        
        

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["username"]
        passw = request.form["password"]
        
        login = User.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            session['username'] = uname
            session['user_id'] = login.id
            session['user_cat'] = login.category
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('user_cat', None)
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        uname = request.form['username']
        mail = request.form['email']
        passw = request.form['password']
        cat = request.form['category']
        numb = request.form['phone']
        rname = request.form['name']
        if (re.search(regex, mail) and ("@miuandes.cl" in mail or  "@uandes.cl" in mail)):
            register = User(username=uname, email=mail, password=passw, category=cat, telefono=numb, nombre=rname)
            session['username'] = uname
            session['user_id'] = register.id
            session['user_cat'] = register.category
            db.session.add(register)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            print("Invalid Email")
            return render_template("register.html")

    return render_template("register.html")



if __name__ =="__main__":
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run()