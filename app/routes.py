import re
from flask import Blueprint, jsonify, request
from app.controllers.user_controller import UserController

from app.models.User import User

api = Blueprint('PaySphereAPI', __name__)

@api.app_errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Ressource non trouvée"}), 404

@api.route('/')
def home():
    return "Bienvenue sur l'API PaySphereDB, documentation : "

@api.route('/users', methods=['GET'])
def all_users():
    users =  UserController.get_all_users()
    return jsonify([u.to_dict() for u in users])

@api.route('/users/<int:user_id>', methods=['GET'])
def user_by_id(user_id):
    try:
        user = UserController.get_user_by_id(user_id)
        if user is None:
            return jsonify({"erreur": "Utilisateur non trouvé"}), 404
        return jsonify(user.to_dict()), 200
    except ValueError:
        return jsonify({"erreur": "ID utilisateur invalide"}), 400
    except Exception as e:
        return jsonify({"erreur": "Erreur interne du serveur", "message": str(e)}), 500


@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    # Vérification des données requises
    if not data or 'nom' not in data or 'prenom' not in data or 'email' not in data or 'username' not in data:
        return jsonify({"erreur": "Missing required fields"}), 400

    # Validation de l'email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
        return jsonify({"erreur": "Invalid email format"}), 400


    user:User = UserController.create_user(data)

    return jsonify(
        {"id": user.id, "nom": user.nom, "prenom": user.prenom, "email": user.email, "username": user.username}), 201
