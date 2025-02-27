from flask import Blueprint, jsonify

api = Blueprint('PaySphereAPI', __name__)

@api.route('/')
def home():
    return "Bienvenue sur l'API PaySphereDB, documentation : "

@api.app_errorhandler(404)
def page_not_found(e):
    return jsonify({"erreur": "Ressource non trouvée"}), 404