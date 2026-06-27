from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity

from app import db, limiter
from app.controllers.client_controller import ClientController
from app.controllers.user_controller import UserController
from app.models.User import User
from app.models.TokenBlacklist import TokenBlacklist
from app.routes import api, jwt
from app.utils.errors import handle_exceptions


@api.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
@handle_exceptions
def register():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"erreur": "Données invalides"}), 400

    user = UserController.get_user_by_username(data['username'])
    if user is None and User.is_schema_valid(data['password']):
        UserController.create_user(data)
        return jsonify({"message": "Utilisateur enregistré"}), 201

    return jsonify({"erreur": "Nom d'utilisateur déjà pris ou mot de passe invalide"}), 400


@api.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
@handle_exceptions
def login():
    data = request.json
    if not data or 'num' not in data or 'password' not in data:
        return jsonify({"erreur": "Données invalides"}), 400

    try:
        num_client = int(data['num'])
    except (ValueError, TypeError):
        return jsonify({"erreur": "Numéro client invalide"}), 400

    client = ClientController.get_client_by_numero(num_client)
    if not client or not client.user:
        return jsonify({"erreur": "Identifiants invalides"}), 401

    user = client.user

    if user.authentification and user.authentification.is_password_valid(data.get('password')):
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200

    return jsonify({"erreur": "Identifiants invalides"}), 401


@api.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)
    return jsonify(access_token=new_access_token), 200


@api.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlacklist(jti=jti))
    db.session.commit()
    return jsonify({"message": "Déconnexion réussie"}), 200


@api.route('/logout_refresh', methods=['POST'])
@jwt_required(refresh=True)
def logout_refresh():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlacklist(jti=jti))
    db.session.commit()
    return jsonify({"message": "Refresh token révoqué"}), 200


@jwt.token_in_blocklist_loader
def check_if_token_is_blacklisted(jwt_header, jwt_data):
    return TokenBlacklist.query.filter_by(jti=jwt_data["jti"]).first() is not None


@api.route('/verifier_code', methods=['POST'])
@jwt_required()
@limiter.limit("5 per minute")
@handle_exceptions
def verifier_code():
    data = request.json
    if not data or 'num' not in data or 'password' not in data:
        return jsonify({"erreur": "Données invalides"}), 400

    try:
        num_client = int(data['num'])
    except (ValueError, TypeError):
        return jsonify({"success": False}), 400

    client = ClientController.get_client_by_numero(num_client)
    if not client or not client.user:
        return jsonify({"success": False}), 401

    user = client.user
    if user.authentification.is_password_valid(data.get('password')):
        return jsonify({"success": True}), 200

    return jsonify({"success": False}), 401
