from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.routes import api
from app.controllers.pret_controller import PretController
from app.controllers.user_controller import UserController


@api.route('/prets', methods=['POST'])
@jwt_required()
def creer_pret():
    current_user_id = int(get_jwt_identity())
    user = UserController.get_user_by_id(current_user_id)

    if not user or not user.client:
        return jsonify({"erreur": "Client introuvable"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"erreur": "Données JSON requises"}), 400

    montant = data.get('montant')
    duree_mois = data.get('duree_mois')

    if montant is None or duree_mois is None:
        return jsonify({"erreur": "Montant et durée requis"}), 400

    try:
        montant = float(montant)
        duree_mois = int(duree_mois)
    except (ValueError, TypeError):
        return jsonify({"erreur": "Montant ou durée invalide"}), 400

    pret, erreur = PretController.creer_pret(user.client, montant, duree_mois)
    if erreur:
        return jsonify({"erreur": erreur}), 400

    return jsonify({"message": "Demande de prêt enregistrée", "pret": pret.to_dict()}), 201


@api.route('/prets', methods=['GET'])
@jwt_required()
def get_prets():
    current_user_id = int(get_jwt_identity())
    user = UserController.get_user_by_id(current_user_id)

    if not user or not user.client:
        return jsonify({"erreur": "Client introuvable"}), 404

    prets = PretController.get_prets_by_client(user.client.id)
    return jsonify({"prets": [p.to_dict() for p in prets]}), 200


@api.route('/prets/<int:pret_id>', methods=['GET'])
@jwt_required()
def get_pret(pret_id):
    current_user_id = int(get_jwt_identity())
    pret = PretController.get_pret_by_id(pret_id)

    if not pret:
        return jsonify({"erreur": "Prêt introuvable"}), 404

    if pret.client.user.get_id() != current_user_id:
        return jsonify({"erreur": "Accès interdit"}), 403

    return jsonify({"pret": pret.to_dict()}), 200


@api.route('/prets/<int:pret_id>/annuler', methods=['POST'])
@jwt_required()
def annuler_pret(pret_id):
    current_user_id = int(get_jwt_identity())
    pret = PretController.get_pret_by_id(pret_id)

    if not pret:
        return jsonify({"erreur": "Prêt introuvable"}), 404

    if pret.client.user.get_id() != current_user_id:
        return jsonify({"erreur": "Accès interdit"}), 403

    success, message = PretController.annuler_pret(pret)
    if not success:
        return jsonify({"erreur": message}), 400

    return jsonify({"message": message}), 200
