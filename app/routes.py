import re
from flask import Blueprint, jsonify, request
from app.controllers.user_controller import UserController

from app.models.User import User
api = Blueprint('PaySphereAPI', __name__)

@api.route('/')
def home():
    return "Bienvenue sur l'API PaySphereDB, documentation : "

@api.route('/users', methods=['GET'])
def all_users():
    users =  UserController.get_all_users()
    return jsonify([u.to_dict() for u in users])


@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    # Vérification des données requises
    if not data or 'nom' not in data or 'prenom' not in data or 'email' not in data or 'username' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    # Validation de l'email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
        return jsonify({"error": "Invalid email format"}), 400


    user:User = UserController.create_user(data)

    return jsonify(
        {"id": user.id, "nom": user.nom, "prenom": user.prenom, "email": user.email, "username": user.username}), 201
