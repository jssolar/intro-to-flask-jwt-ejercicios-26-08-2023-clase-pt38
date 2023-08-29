import os
import datetime
from flask import  Flask, request, jsonify 
from models import db, User
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity, create_access_token, jwt_required
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db.init_app(app)
Migrate(app, db) # flask db init, flask db migrate, flask db upgrade
jwt=JWTManager(app)
CORS(app)

"""
hasta aquí está configurado el modelo con la aplicacion y jwt con mi aplicacion. ya puedo utilizar las dos librerias como quiera
"""

@app.route('/')
def main():
    return jsonify({"message": "API REST CON JWT, CHAVALETE!!!!"})

# generar ruta para el registro

@app.route('/api/register', methods=['POST'])
def register():
    username= request.json.get("username")
    password= request.json.get("password")

    # validacion de usuario
    if not username:
        return jsonify({"error": "username is requare"}), 422
    
    if not password:
        return jsonify({"error": "password is requare"}), 422
    
    # creacion de usuario
    
    userFaund = User.query.filter_by(username=username).first()
    
    if not username:
        return jsonify({"error": "username esta siendo usado"}), 400
    user = User() 
    user.username = username 
    user.password = generate_password_hash(password) 
    user.save()
    
    return jsonify({"succes": "Registro exitoso, por favor inicie sesión"}), 200

@app.route('/api/login', methods=['POST'])
def login():
    
    username= request.json.get("username")
    password= request.json.get("password")

    # validacion de usuario, de datos ingresados
    if not username:
        return jsonify({"error": "username is requare"}), 422
    
    if not password:
        return jsonify({"error": "password is requare"}), 422

# BUSCAMOS AL USUARIO
    user = User.query.filter_by(username=username).first()
    
# SI NO EXISTE EL USUARIO
    if not user: 
        return jsonify({"message": "tu usuario o contraseña son incorrectos"}), 401
    
# LAVIDAMOS LA CONTRASEÑA
    if not check_password_hash(user.password, password):
        return jsonify({"message": "tu usuario o contraseña son incorrectos"}), 401 
        

# generacion/creacion de token
# antes de generar el token, genero una variable
# expires = datetime.timedelta(days=6)
# access_token = create_access_token(identity=user.id, expires_delta=expires)
    access_token = create_access_token(identity=user.id)
    
    data = {
        "access_token": access_token,
        "type": "Bearer",
        "user": user.serialize()
    }


    return jsonify(data), 200


# generando ruta privada
@app.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
    
    id = get_jwt_identity()
    user = User.query.get(id)
    return jsonify({"message": "ruta  privada", "user": user.username}), 200






if __name__ == '__main__':
    app.run()