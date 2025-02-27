from flask import Blueprint, request, jsonify
from app.controllers.virement_controller import VirementController

virement_bp = Blueprint('virement_bp', __name__)

@virement_bp.route('/virement', methods=['POST'])
def create_virement():
    data = request.get_json()
    virement, message = VirementController.create_virement(data)

    if not virement:
        return jsonify({"success": False, "message": message}), 400

    return jsonify({
        "success": True,
        "message": message,
        "data": virement.to_dict()
    }), 201
