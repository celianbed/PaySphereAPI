from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app.routes import api
from ..controllers.client_controller import ClientController
from ..utils.errors import handle_exceptions


@api.route('/clients', methods=['POST'])
@handle_exceptions
def create_client():
    data = request.get_json()
    if not data:
        return jsonify({"erreur": "Données JSON requises"}), 400
    client = ClientController.create_client(data)
    return jsonify(client.to_dict()), 201


@api.route('/clients/<int:client_id>', methods=['GET'])
@handle_exceptions
@jwt_required()
def get_client_by_id(client_id):
    client = ClientController.get_client_by_id(client_id)

    if client is None:
        return jsonify({"erreur": "Utilisateur non trouvé"}), 404

    fields = request.args.get('fields')

    if fields:
        fields_list = fields.split(',')
        fields_list =[fild.lower() for fild in fields_list]
    else:
        fields_list = None


    return jsonify(client.to_dict(fields=fields_list)), 200


@api.route('/clients/numero/<string:numero_client>', methods=['GET'])
@handle_exceptions
@jwt_required()
def get_client_by_numero(numero_client):
    client = ClientController.get_client_by_numero(numero_client)

    if client is None:
        return jsonify({"erreur": "Utilisateur non trouvé"}), 404

    fields = request.args.get('fields')

    if fields:
        fields_list = fields.split(',')
        fields_list =[fild.lower() for fild in fields_list]
    else:
        fields_list = None


    return jsonify(client.to_dict(fields_list)), 200