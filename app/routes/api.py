from flask import jsonify, Blueprint, redirect
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail


api = Blueprint('PaySphereAPI', __name__)
jwt = JWTManager()
mail = Mail()
bcrypt = Bcrypt()

@api.route('/')
def home():
    return "Bienvenue sur l'API PaySphereDB, appuyer ici pour la documentation "

@api.route('/documentation')
def swagger():
    return redirect("/swagger")

@api.app_errorhandler(404)
def page_not_found(e):
    return jsonify({"erreur": "Ressource non trouvée"}), 404

