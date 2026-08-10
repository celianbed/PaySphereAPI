from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app.controllers.virement_controller import VirementController
from app.routes import api
from app.utils.authz import current_client, owned_compte
from app.utils.errors import handle_exceptions


@api.route('/virement', methods=['POST'])
@jwt_required()
@handle_exceptions
def create_virement():
    """
    Émet un virement depuis un compte appartenant à l'utilisateur connecté.

    L'autorisation repose sur la résolution du compte émetteur puis sur la
    vérification de son propriétaire ; l'identifiant transmis par le client
    n'est jamais comparé directement à l'identité du porteur du jeton.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "Données JSON requises"}), 400

    if data.get('from_account') is None:
        return jsonify({"success": False, "message": "Le compte émetteur est requis"}), 400

    # Lève NotFoundError si le compte n'existe pas ou n'appartient pas à
    # l'appelant : les deux cas sont volontairement indiscernables.
    compte_source = owned_compte(data['from_account'])

    # On réinjecte l'identifiant vérifié plutôt que celui reçu, afin que le
    # contrôleur ne puisse pas travailler sur un autre compte que celui validé.
    virement_eff, message, virement = VirementController.create_virement(
        {**data, 'from_account': compte_source.get_id()}
    )

    if not virement_eff:
        return jsonify({"success": False, "message": message}), 400

    return jsonify({
        "success": True,
        "message": message,
        "data": virement.to_dict(),
    }), 201


@api.route('/virement', methods=['GET'])
@jwt_required()
@handle_exceptions
def get_virement():
    """
    Retourne les virements émis ou reçus par les comptes de l'appelant.

    Paramètres de requête : ``page`` (défaut 1) et ``per_page`` (défaut 20,
    plafonné à 100).
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    page = max(page, 1)
    per_page = min(max(per_page, 1), 100)

    client = current_client()
    virements = VirementController.get_virements_by_client(client.id)

    total = len(virements)
    start = (page - 1) * per_page
    end = start + per_page

    return jsonify({
        "data": [v.to_dict() for v in virements[start:end]],
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": (total + per_page - 1) // per_page
    }), 200


@api.route("/virements/verifie-beneficiaire", methods=["POST"])
@jwt_required()
@handle_exceptions
def check_beneficiaire():
    """Vérifie qu'un IBAN correspond à un compte pouvant recevoir un virement."""
    data = request.get_json(silent=True) or {}
    iban = data.get("to_account_iban")

    if not iban:
        return jsonify({"valid": False, "message": "IBAN manquant"}), 400

    exists = VirementController.verifier_beneficiaire_existant(iban)
    if exists:
        return jsonify({"valid": True}), 200
    else:
        return jsonify({"valid": False, "message": "Bénéficiaire introuvable"}), 404
