from flask import jsonify,request
from flask_jwt_extended import jwt_required

from .api import api
from app.controllers.compte_controller import CompteController
from app.utils.errors import handle_exceptions


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
    fields = request.args.get('fields')
    exclude = request.args.get('exclude')

    if fields:
        fields_list = fields.split(',')
        fields_list =[fild.lower() for fild in fields_list]
    else:
        fields_list = None

    if exclude:
        exclude_list = exclude.split(',')
        exclude_list = [exclude.lower() for exclude in exclude_list]
    else:
        exclude_list = None

    compte = CompteController.get_compte_by_id(compte_id)
    return jsonify(compte.to_dict(fields=fields_list,exclude=exclude_list)), 200