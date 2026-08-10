from flask import jsonify, request
from flask_jwt_extended import jwt_required

from app.controllers.compte_controller import CompteController
from app.routes import api
from app.utils.authz import current_client, owned_compte
from app.utils.errors import handle_exceptions


def _parse_field_filters():
    """
    Lit les paramètres ``fields`` et ``exclude`` de la requête courante.

    :return: Un couple ``(fields, exclude)``, chaque élément étant une liste de
     noms de champs en minuscules ou ``None`` si le paramètre est absent.
    """
    fields = request.args.get('fields')
    exclude = request.args.get('exclude')

    fields_list = [f.strip().lower() for f in fields.split(',')] if fields else None
    exclude_list = [e.strip().lower() for e in exclude.split(',')] if exclude else None

    return fields_list, exclude_list


@api.route('/comptes', methods=['GET'])
@jwt_required()
@handle_exceptions
def get_all_compte():
    """
    Retourne les comptes du client connecté.

    Cette route retournait auparavant l'intégralité de la table ``compte``,
    exposant le solde, l'IBAN et le titulaire de tous les clients à n'importe
    quel porteur de jeton valide.
    """
    fields_list, exclude_list = _parse_field_filters()

    client = current_client()
    comptes = CompteController.get_comptes_by_client(client.id)

    return jsonify([
        compte.to_dict(fields=fields_list, exclude=exclude_list)
        for compte in comptes
    ]), 200


@api.route('/comptes', methods=['POST'])
@jwt_required()
@handle_exceptions
def create_compte():
    """
    Ouvre un nouveau compte pour le client connecté.

    Le titulaire n'est pas lu dans le corps de la requête : un client ne peut
    ouvrir un compte que pour lui-même.
    """
    client = current_client()
    compte = CompteController.create_compte(client)
    return jsonify(compte.to_dict()), 201


@api.route('/comptes/<int:compte_id>', methods=['GET'])
@jwt_required()
@handle_exceptions
def get_compte(compte_id):
    """Retourne le détail d'un compte appartenant à l'utilisateur connecté."""
    compte = owned_compte(compte_id)
    fields_list, exclude_list = _parse_field_filters()

    return jsonify(compte.to_dict(fields=fields_list, exclude=exclude_list)), 200
