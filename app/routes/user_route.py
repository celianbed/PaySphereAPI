from flask import jsonify, request
from app.controllers.user_controller import UserController
from app.models.User import User
from app.utils.errors import handle_exceptions
from .api import api




@api.route('/users', methods=['GET'])
@handle_exceptions
def all_users():
    users = UserController.get_all_users()
    return jsonify([u.to_dict() for u in users]), 200


@api.route('/users', methods=['POST'])
@handle_exceptions
def new_user():
    data = request.get_json()
    if not data:
        return jsonify({"erreur": "Données JSON requises"}), 400

    status, response = User.verif_data(data)
    if status:
        return jsonify(response["erreur"]), 400

    if not User.is_email_valid(data.get("email", "")):
        return jsonify({"erreur": "Format de mail invalide"}), 400

    user, auth = UserController.create_user(data)
    return jsonify(user.to_dict(), auth.to_dict()), 201


@api.route('/users/<int:user_id>', methods=['GET', 'PATCH', 'DELETE'])
@handle_exceptions
def user_operations(user_id):
    user = UserController.get_user_by_id(user_id)
    if user is None:
        return jsonify({"erreur": "Utilisateur non trouvé"}), 404

    if request.method == 'GET':
        return jsonify(user.to_dict()), 200

    if request.method == 'PATCH':
        data = request.get_json()
        if not data:
            return jsonify({"erreur": "Données JSON requises"}), 400
        UserController.update_user(user, data)
        return jsonify(user.to_dict()), 200

    if request.method == 'DELETE':
        if UserController.delete_user(user):
            return jsonify({"message": "Utilisateur bien supprimé"}), 200



