"""
Routes de gestion du compte utilisateur.

Toutes les routes de ce module portent sur l'utilisateur authentifié lui-même.
Le contrôle ``user_id != current_user_id`` répond ``403`` sans consulter la base
: la réponse est donc identique que l'identifiant demandé existe ou non, et ne
permet pas d'énumérer les utilisateurs.

La création d'un compte se fait exclusivement par ``POST /register``, qui
applique la limitation de débit et la politique de mot de passe. Les anciennes
routes ``GET /users`` (qui retournait tous les utilisateurs et leurs adresses
e-mail) et ``POST /users`` (création arbitraire d'utilisateur par tout porteur
de jeton) ont été retirées : elles n'avaient aucun usage applicatif et
l'API ne dispose d'aucun modèle de rôles permettant de les encadrer.
"""

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.controllers.user_controller import UserController
from app.models.User import User
from app.utils.errors import handle_exceptions
from .api import api


@api.route('/users/<int:user_id>', methods=['GET', 'PATCH', 'DELETE'])
@jwt_required()
@handle_exceptions
def user_operations(user_id):
    """Consulte, modifie ou supprime le compte de l'utilisateur connecté."""
    current_user_id = int(get_jwt_identity())
    if user_id != current_user_id:
        return jsonify({"erreur": "Accès interdit"}), 403

    user = UserController.get_user_by_id(user_id)
    if user is None:
        return jsonify({"erreur": "Utilisateur non trouvé"}), 404

    if request.method == 'GET':
        fields = request.args.get('fields')
        fields_list = [f.strip().lower() for f in fields.split(',')] if fields else None
        return jsonify(user.to_dict(fields=fields_list)), 200

    if request.method == 'PATCH':
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"erreur": "Données JSON requises"}), 400
        allowed = {'nom', 'prenom', 'email'}
        filtered = {k: v for k, v in data.items() if k in allowed}
        if not filtered:
            return jsonify({"erreur": "Aucun champ modifiable fourni"}), 400
        if 'email' in filtered and not User.is_email_valid(filtered['email']):
            return jsonify({"erreur": "Format de mail invalide"}), 400
        UserController.update_user(user, filtered)
        return jsonify(user.to_dict()), 200

    if request.method == 'DELETE':
        UserController.delete_user(user)
        return jsonify({"message": "Utilisateur supprimé"}), 200


@api.route('/users/<int:user_id>/change-password', methods=['PATCH'])
@jwt_required()
@handle_exceptions
def changer_mot_de_passe_route(user_id):
    """Change le mot de passe de l'utilisateur connecté."""
    user_connecte_id = int(get_jwt_identity())
    if user_id != user_connecte_id:
        return jsonify({"error": "Accès interdit"}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Données JSON manquantes"}), 400

    ancien = data.get('ancien_password')
    nouveau = data.get('nouveau_password')

    if not ancien or not nouveau:
        return jsonify({"error": "Les champs 'ancien_password' et 'nouveau_password' sont requis"}), 400

    if not User.is_schema_valid(nouveau):
        return jsonify({"error": "Le nouveau mot de passe ne respecte pas les critères de sécurité (12-20 car., maj, min, chiffre, symbole)"}), 400

    result, status_code = UserController.changer_mot_de_passe(user_id, ancien, nouveau)
    return jsonify(result), status_code
