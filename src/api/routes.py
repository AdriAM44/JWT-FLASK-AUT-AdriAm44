"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200


# [POST] /api/signup - Registro de usuario
@api.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "Cuerpo de la petición vacío"}), 400

    email = body.get('email')
    password = body.get('password')

    if not email or not password:
        return jsonify({"msg": "Email y contraseña son obligatorios"}), 400

    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        return jsonify({"msg": "El usuario ya existe"}), 400

    new_user = User(email=email, password=password, is_active=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuario creado con éxito"}), 201


# [POST] /api/login - Inicio de sesión
@api.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "Cuerpo de la petición vacío"}), 400

    email = body.get('email')
    password = body.get('password')

    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return jsonify({"msg": "Credenciales incorrectas"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"token": access_token, "user_id": user.id}), 200


# [GET] /api/private - Ruta protegida
@api.route('/private', methods=['GET'])
@jwt_required()
def private():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    return jsonify({"logged_in_as": user.email, "msg": "Acceso concedido a la vista privada"}), 200
