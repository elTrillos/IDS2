from unicodedata import category
from app import db, User, Emprendimiento, Puntuacion, Producto

u1=User(id=2,username="xd",password="123123", category="user", nombre="Pedrito", email="elp@gmail.com")
u2=User(id=3,username="elMismisimo",password="123123", category="user", nombre="Checo", email="checoo@gmail.com")
u3=User(id=4,username="lePepe",password="123123", category="user", nombre="Pepe", email="elpepe@gmail.com")
db.session.add_all([u1,u2,u3])
print("xdddd")
print(u1.id)
e1=Emprendimiento(id=1,id_usuario=u1.id, nombre="nanai", descripcion="xd pdi")
e2=Emprendimiento(id=2,id_usuario=u2.id, nombre="puroperkin", descripcion="xd pdi")

p1=Producto(nombre="prod1", disponibilidad=25, precio=5000,id_emprendimiento=e1.id)
p2=Producto(nombre="prod2", disponibilidad=24, precio=500045,id_emprendimiento=e1.id)
p3=Producto(nombre="prod3", disponibilidad=2, precio=12,id_emprendimiento=e2.id)
p4=Producto(nombre="prod4", disponibilidad=5, precio=230,id_emprendimiento=e2.id)

db.session.add_all([e1,e2])
db.session.add_all([p1, p2,p3,p4])


db.session.commit()
