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