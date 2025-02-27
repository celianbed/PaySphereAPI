from flask import request, jsonify
from .api import api
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
