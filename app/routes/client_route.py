from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.routes import api
from ..controllers.client_controller import ClientController
from ..models.Beneficiaire import Beneficiaire
from ..utils.errors import handle_exceptions


@api.route('/clients', methods=['POST'])
@jwt_required()
@handle_exceptions
def create_client():
    data = request.get_json()
    if not data:
        return jsonify({"erreur": "Données JSON requises"}), 400
    client = ClientController.create_client(data)
    return jsonify(client.to_dict()), 201


@api.route('/clients/<int:client_id>', methods=['GET'])
@jwt_required()
@handle_exceptions
def get_client_by_id(client_id):
    current_user_id = int(get_jwt_identity())
    client = ClientController.get_client_by_id(client_id)

    if client is None:
        return jsonify({"erreur": "Client non trouvé"}), 404

    if client.user.get_id() != current_user_id:
        return jsonify({"erreur": "Accès interdit"}), 403

    fields = request.args.get('fields')
    fields_list = [f.strip().lower() for f in fields.split(',')] if fields else None

    return jsonify(client.to_dict(fields=fields_list)), 200


@api.route('/clients/numero/<string:numero_client>', methods=['GET'])
@jwt_required()
@handle_exceptions
def get_client_by_numero(numero_client):
    current_user_id = int(get_jwt_identity())
    client = ClientController.get_client_by_numero(numero_client)

    if client is None:
        return jsonify({"erreur": "Client non trouvé"}), 404

    if client.user.get_id() != current_user_id:
        return jsonify({"erreur": "Accès interdit"}), 403

    fields = request.args.get('fields')
    fields_list = [f.strip().lower() for f in fields.split(',')] if fields else None

    return jsonify(client.to_dict(fields_list)), 200


@api.route('/clients/beneficiaires', methods=['POST'])
@jwt_required()
def ajouter_beneficiaire():
    data = request.get_json()
    iban = data.get('iban')
    nom = data.get('nom')

    if not iban or not nom:
        return jsonify({"error": "Nom et IBAN requis"}), 400

    current_user_id = int(get_jwt_identity())
    from app.controllers.user_controller import UserController
    user = UserController.get_user_by_id(current_user_id)
    if not user or not user.client:
        return jsonify({"error": "Client introuvable"}), 404

    client = user.client

    if Beneficiaire.query.filter_by(iban=iban, client_id=client.id).first():
        return jsonify({"error": "Ce bénéficiaire existe déjà"}), 400

    benef = ClientController.creer_beneficiaire(iban, nom, client)

    return jsonify({
        "message": "Bénéficiaire ajouté",
        "beneficiaire": benef.to_dict()
    }), 201


@api.route('/clients/<int:client_id>', methods=['PATCH', 'DELETE'])
@jwt_required()
def modifier_client(client_id):
    current_user_id = int(get_jwt_identity())
    client = ClientController.get_client_by_id(client_id)

    if client is None:
        return jsonify({"erreur": "Client non trouvé"}), 404

    if client.user.get_id() != current_user_id:
        return jsonify({"erreur": "Accès interdit"}), 403

    if request.method == 'PATCH':
        data = request.get_json()
        if not data:
            return jsonify({"erreur": "Données JSON requises"}), 400
        allowed = {'nom', 'prenom', 'adresse', 'numero_de_telephone'}
        filtered = {k: v for k, v in data.items() if k in allowed}
        if not filtered:
            return jsonify({"erreur": "Aucun champ modifiable fourni"}), 400
        ClientController.update_client(client, filtered)
        return jsonify(client.to_dict()), 200

    if request.method == 'DELETE':
        ClientController.delete_client(client)
        return jsonify({"message": "Client supprimé"}), 200


@api.route('/clients/beneficiaires/<int:beneficiaire_id>', methods=['DELETE'])
@jwt_required()
def delete_beneficiaire(beneficiaire_id):
    current_user_id = int(get_jwt_identity())
    beneficiaire = Beneficiaire.query.get(beneficiaire_id)

    if not beneficiaire:
        return jsonify({"erreur": "Bénéficiaire introuvable"}), 404

    if beneficiaire.client.user.get_id() != current_user_id:
        return jsonify({"erreur": "Accès interdit"}), 403

    return ClientController.supprimer_beneficiaire(beneficiaire_id)
