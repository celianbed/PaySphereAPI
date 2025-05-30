from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.routes import api
from ..controllers.client_controller import ClientController
from ..models.Beneficiaire import Beneficiaire
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



@api.route('/clients/beneficiaires', methods=['POST'])
@jwt_required()
def ajouter_beneficiaire():
    data = request.get_json()
    iban = data.get('iban')
    nom = data.get('nom')

    if not iban or not nom:
        return jsonify({"error": "Nom et IBAN requis"}), 400

    if Beneficiaire.query.filter_by(iban=iban).first():
        return jsonify({"error": "Ce bénéficiaire existe déjà"}), 400

    client_id = get_jwt_identity()
    client = ClientController.get_client_by_id(client_id)

    if not client:
        return jsonify({"error": "Client introuvable"}), 404

    benef = ClientController.creer_beneficiaire(iban, nom, client)

    return jsonify({
        "message": "Bénéficiaire ajouté",
        "beneficiaire": {
            "id": benef.id,
            "nom": benef.nom,
            "iban": benef.iban
        }
    }), 201


@api.route('/clients/<int:client_id>', methods=['GET', 'PATCH', 'DELETE'])
@jwt_required()
def modifier_client(client_id):
    client = ClientController.get_client_by_id(client_id)

    fields = request.args.get('fields')

    if fields:
        fields_list = fields.split(',')
        fields_list =[fild.lower() for fild in fields_list]
    else:
        fields_list = None


    if client is None:
        return jsonify({"erreur": "Client non trouvé"}), 404,{'Content-Type': 'application/json; charset=utf-8'}

    if request.method == 'GET':
        return jsonify(client.to_dict(fields=fields_list)), 200

    if request.method == 'PATCH':
        data = request.get_json()
        if not data:
            return jsonify({"erreur": "Données JSON requises"}), 400
        ClientController.update_client(client, data)
        return jsonify(client.to_dict()), 200

    if request.method == 'DELETE':
        if ClientController.delete_client(client):
            return jsonify({"message": "Utilisateur bien supprimé"}), 200

@api.route('/clients/beneficiaires/<int:beneficiaire_id>', methods=['DELETE'])
@jwt_required()
def delete_beneficiaire(beneficiaire_id):
    return ClientController.supprimer_beneficiaire(beneficiaire_id)
