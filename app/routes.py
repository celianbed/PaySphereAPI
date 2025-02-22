from flask import Blueprint, jsonify, request

from app.controllers.compte_controller import CompteController
from app.controllers.user_controller import UserController
from app.models.User import User
from app.utils.errors import handle_exceptions
from flask_login import LoginManager


api = Blueprint('PaySphereAPI', __name__)

@api.app_errorhandler(404)
def page_not_found(e):
    return jsonify({"erreur": "Ressource non trouvée"}), 404

@api.route('/')
def home():
    return "Bienvenue sur l'API PaySphereDB, documentation : "

@api.route('/users', methods=['GET'])
def all_users():
    users =  UserController.get_all_users()
    return jsonify([u.to_dict() for u in users])

@api.route('/users', methods=['POST'])
@handle_exceptions
def create_user():
    data = request.get_json()
    status,response = User.verif_data(data)

    if status:
        return jsonify(response["erreur"]), 400
    if not User.is_email_valid(data["email"]):
        return jsonify({"erreur": "Invalid email format"}), 400

    user, auth = UserController.create_user(data)
    return jsonify(user.to_dict(), auth.to_dict()), 201


@api.route('/users/<int:user_id>', methods=['GET'])
@handle_exceptions
def user_by_id(user_id):
        user = UserController.get_user_by_id(user_id)
        if user is None:
            return jsonify({"erreur": "Utilisateur non trouvé"}), 404
        return jsonify(user.to_dict()), 200



@api.route('/users/<int:user_id>', methods=['PATCH'])
@handle_exceptions
def maj_user(user_id: int):
    data = request.get_json()
    user = UserController.get_user_by_id(user_id)
    if user is None:
        return jsonify({"erreur": "Utilisateur non trouvé"}), 404
    UserController.update_user(user, data)
    return jsonify(user.to_dict()), 200

@api.route('/users/<int:user_id>', methods=['DELETE'])
@handle_exceptions
def delete_user(user_id: int):
    user = UserController.get_user_by_id(user_id)
    if user is None:
        return jsonify({"erreur": "Utilisateur non trouvé"}), 404
    if UserController.delete_user(user):
        return jsonify({"message":"Utilisateur bien supprimé"})





@api.route('/comptes', methods=['GET'])
@handle_exceptions
def get_compte():
    comptes = CompteController.get_all_comptes()
    return jsonify([compte.to_dict() for compte in comptes]), 200

@api.route('/comptes', methods=['POST'])
@handle_exceptions
def create_compte(data):
    compte = CompteController.create_compte(data)
    return jsonify(compte.to_dict()), 201