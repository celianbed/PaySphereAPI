    from flask import jsonify
    from .api import api
    from app.controllers.compte_controller import CompteController
    from app.utils.errors import handle_exceptions


    @api.route('/comptes', methods=['GET'])
    @handle_exceptions
    def get_compte():
        comptes = CompteController.get_all_comptes()
        return jsonify([compte.to_dict() for compte in comptes]), 200

    @api.route('/comptes', methods=['POST'])
    @handle_exceptions
    def create_compte(data):
        compte = CompteController.create_compte(data)
        return jsonify(compte.to_dict()), 201