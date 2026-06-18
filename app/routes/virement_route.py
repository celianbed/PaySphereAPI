from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.virement_controller import VirementController
from app.routes import api


@api.route('/virement', methods=['POST'])
@jwt_required()
def create_virement():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()

    if data["from_account"] != current_user_id:
        return jsonify({"success": False, "message": "Accès non autorisé"}), 403

    try:
        virement_eff, message, virement = VirementController.create_virement(data)
        return jsonify({
            "success": virement_eff,
            "message": message,
            "data": virement.to_dict()
        }), 201
    except ValueError:
        virement_eff, message = VirementController.create_virement(data)
        return jsonify({"success": virement_eff, "message": message}), 400


@api.route('/virement', methods=['GET'])
@jwt_required()
def get_virement():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)

    virements = VirementController.get_all_virements()
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
def check_beneficiaire():
    data = request.get_json()
    iban = data.get("to_account_iban")

    if not iban:
        return jsonify({"valid": False, "message": "IBAN manquant"}), 400

    exists = VirementController.verifier_beneficiaire_existant(iban)
    if exists:
        return jsonify({"valid": True}), 200
    else:
        return jsonify({"valid": False, "message": "Bénéficiaire introuvable"}), 404
