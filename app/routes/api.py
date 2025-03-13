from flask import jsonify, Blueprint
from flask_jwt_extended import JWTManager

from app.controllers.authentification_controller import AuthentificationController

api = Blueprint('PaySphereAPI', __name__)
jwt = JWTManager()


@api.route('/')
def home():
    return "Bienvenue sur l'API PaySphereDB, documentation : "

@api.app_errorhandler(404)
def page_not_found(e):
    return jsonify({"erreur": "Ressource non trouvée"}), 404

@api.route('/hash_mdp')
def hash_mdp():

    AuthentificationController.create_auth()