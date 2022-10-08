# IDS

## Tutorial instalar environment:
### crear el ambiente
python3 -m venv venv 
### entrar en el ambiente
#### WSL
source venv/bin/activate
#### Windows
venv\Scripts\activate.bat
### instalar cosas
pip install Flask
pip install flask-sqlalchemy
### clonar el ambiente
#### se debe tomar todo lo dentro de la carpeta IDS y pasarla a la carpeta de arriba, y borrar lo que queda adentro

### correr el codigo
flask --app app.py --debug run

### llenar base de datos (WIP pocos datos pero funca)
python3 prefill_db.py

## Inicializar la base de datos
1. Borrar archivo instance/test.db
```
>python3
from app import db
db.create_all()
```
### Para poner datos precreados
```
>python3
prefill_db.py
```