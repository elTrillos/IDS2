from unicodedata import category
from app import EmprendimientoImage, ProductImage, db, User, Emprendimiento, Puntuacion, Producto

u1=User(id=2,username="xd",password="123123", category="user", nombre="Pedrito", email="elp@gmail.com")
u2=User(id=3,username="elMismisimo",password="123123", category="user", nombre="Checo", email="checoo@gmail.com")
u3=User(id=4,username="lePepe",password="123123", category="user", nombre="Pepe", email="elpepe@gmail.com")
db.session.add_all([u1,u2,u3])
print("xdddd")
print(u1.id)
e1=Emprendimiento(id=1,id_usuario=u1.id, nombre="nanai", descripcion="xd pdi", categoria="gente",imagen_name="1.jpg")
e2=Emprendimiento(id=2,id_usuario=u2.id, nombre="puroperkin", descripcion="xd pdi", categoria="autos")
ei1=EmprendimientoImage(id=1,imagename="1.jpg", id_emprendimiento=e1.id)
p1=Producto(nombre="prod1",descripcion="El producto uno es xd", disponibilidad=25, precio=5000,id_emprendimiento=e1.id,imagen_name="0grs8wpn1wx41.jpg")
p2=Producto(nombre="prod2",descripcion="El producto dos es xd", disponibilidad=24, precio=500045,id_emprendimiento=e1.id)
p3=Producto(nombre="prod3",descripcion="El producto tres es xd", disponibilidad=2, precio=12,id_emprendimiento=e2.id)
p4=Producto(nombre="prod4",descripcion="Ok este producto es enserio 10/10 compralo", disponibilidad=5, precio=230,id_emprendimiento=e2.id)
pi1=ProductImage(id=1,imagename="0grs8wpn1wx41.jpg", id_producto=e1.id)

db.session.add_all([e1,e2])
db.session.add_all([p1, p2,p3,p4])
db.session.add_all([pi1,ei1])

db.session.commit()
