from unicodedata import category
from app import db, User, Emprendimiento, Puntuacion, Producto

u1=User(id=2,username="xd",password="123123", category="user", nombre="Pedrito", email="elp@gmail.com")
db.session.add_all([u1])
print("xdddd")
print(u1.id)
e1=Emprendimiento(id=1,id_usuario=u1.id, nombre="nanai", descripcion="xd pdi")

p1=Producto(nombre="xd", disponibilidad=25, precio=5000,id_emprendimiento=e1.id)
p2=Producto(nombre="xd2", disponibilidad=24, precio=500045,id_emprendimiento=e1.id)

db.session.add_all([e1])
db.session.add_all([p1, p2])


db.session.commit()