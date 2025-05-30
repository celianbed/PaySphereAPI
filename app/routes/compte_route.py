from flask import jsonify,request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from .api import api
from app.controllers.compte_controller import CompteController
from ..models import Compte, Client
from ..utils.errors import handle_exceptions


@api.route('/comptes', methods=['GET'])
def get_all_compte():
    comptes = CompteController.get_all_comptes()
    return jsonify([compte.to_dict() for compte in comptes]), 200



@api.route('/comptes', methods=['POST'])
@handle_exceptions
def create_compte(data):
    compte = CompteController.create_compte(data)
    return jsonify(compte.to_dict()), 201


@api.route('/comptes/<int:compte_id>', methods=['GET'])
@jwt_required()
def get_compte(compte_id):
    user_id = int(get_jwt_identity())


    # Récupération du compte
    compte:Compte = CompteController.get_compte_by_id(compte_id)

    if not compte:
        return jsonify({"error": "Compte introuvable"}), 404

    # Vérification que ce compte appartient bien à l'utilisateur connecté
    if compte.client.user.get_id() != user_id:
        return jsonify({"error": "Accès interdit"}), 403

    # Gestion des paramètres fields / exclude
    fields = request.args.get('fields')
    exclude = request.args.get('exclude')

    if fields:
        fields_list = [f.strip().lower() for f in fields.split(',')]
    else:
        fields_list = None

    if exclude:
        exclude_list = [e.strip().lower() for e in exclude.split(',')]
    else:
        exclude_list = None

    return jsonify(compte.to_dict(fields=fields_list, exclude=exclude_list)), 200







