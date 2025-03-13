import uuid
from dataclasses import field

from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity,get_jwt

from app.controllers.client_controller import ClientController
from app.controllers.user_controller import UserController
from app.models.Client import Client
from app.models.User import User
from app.routes import api,jwt
from app.utils.errors import handle_exceptions

blacklisted_tokens = set()

@api.route('/register', methods=['POST'])
@handle_exceptions
def register():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Données invalides"}), 400

    user = UserController.get_user_by_username(data['username'])
    if user is None and User.is_schema_valid(data['password']) :
        UserController.create_user(data)
        return jsonify({"message": "Utilisateur enregistré"}), 201

    return jsonify({"error": "Nom d'utilisateur déjà pris ou mot de passe invalide"}), 400

@api.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'num' not in data or 'password' not in data:
        return jsonify({"error": "Données invalides"}), 400

    client = ClientController.get_client_by_numero(data['num'])
    user = client.user

    if user and user.authentification.is_password_valid(data.get('password')):
        access_jti = str(uuid.uuid4())
        refresh_jti = str(uuid.uuid4())

        access_token = create_access_token(identity=str(user.id), additional_claims={"jti": access_jti})
        refresh_token = create_refresh_token(identity=str(user.id), additional_claims={"jti": refresh_jti})

        return jsonify(access_token=access_token, refresh_token=refresh_token), 200

    return jsonify({"erreur": "Identifiants invalides"}), 401

@api.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Récupérer le JTI du token actuel
    blacklisted_tokens.add(jti)  # Ajouter à la blacklist
    return jsonify({"message": "Déconnexion réussie"}), 200

@api.route('/logout_refresh', methods=['POST'])
@jwt_required(refresh=True)
def logout_refresh():
    jti = get_jwt()["jti"]
    blacklisted_tokens.add(jti)
    return jsonify({"message": "Refresh token révoqué"}), 200

@jwt.token_in_blocklist_loader
def check_if_token_is_blacklisted(jwt_header, jwt_data):
    return jwt_data["jti"] in blacklisted_tokens
