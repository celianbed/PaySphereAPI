from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.virement_controller import VirementController
from app.routes import api



@api.route('/virement', methods=['POST'])
@jwt_required()  # Exige un token JWT valide pour accéder à cette route
def create_virement():
    current_user = get_jwt_identity() # Récupère les données du token
    id_client = int(current_user)  # On récupère l'id du client depuis le JWT // NON
    data = request.get_json()

    # Vérifier si l'ID du client correspond bien au sender_id
    if data["from_account"] != id_client:
        return jsonify({"success": False, "message": "Accès non autorisé"}), 403

    try :
        virement_eff, message,virement = VirementController.create_virement(data)
        return jsonify({
            "success": virement_eff,
            "message": message,
            "data": virement.to_dict()
        }), 201


    except ValueError :
        virement_eff, message = VirementController.create_virement(data)
        return jsonify({"success": virement_eff, "message": message}), 400


@api.route('/virement', methods=['GET'])
def get_virement():

    virements = VirementController.get_all_virements()
    return jsonify([v.to_dict() for v in virements]), 200

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