from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .api import api
from .. import db
from ..controllers.carte_controller import CarteController
from ..models.Carte import Carte


def _verify_carte_ownership(carte_id):
    """Vérifie que la carte appartient à l'utilisateur connecté."""
    current_user_id = int(get_jwt_identity())
    carte = CarteController.get_carte_by_id(carte_id)
    if not carte:
        return None, jsonify({'error': 'Carte introuvable'}), 404
    if carte.compte.client.user.get_id() != current_user_id:
        return None, jsonify({'error': 'Accès interdit'}), 403
    return carte, None, None


@api.route('/cartes/<int:carte_id>/opposee', methods=['POST'])
@jwt_required()
def opposer_carte(carte_id):
    carte, *err = _verify_carte_ownership(carte_id)
    if not carte:
        return err[0], err[1]

    carte.active = False
    db.session.commit()
    return jsonify({'success': True, 'carte': carte.to_dict()}), 200


@api.route('/cartes/<int:carte_id>/plafond', methods=['GET'])
@jwt_required()
def get_utilisation_plafond(carte_id):
    carte, *err = _verify_carte_ownership(carte_id)
    if not carte:
        return err[0], err[1]

    totale_depense, reste, pourcentage = CarteController.calculer_utilisation_plafond(carte_id)
    return jsonify({
        'total_utilise': round(float(totale_depense), 2),
        'reste': round(float(reste), 2),
        'pourcentage': round(float(pourcentage), 2)
    }), 200


@api.route('/cartes/<int:carte_id>/plafond', methods=['PATCH'])
@jwt_required()
def set_plafond(carte_id):
    carte, *err = _verify_carte_ownership(carte_id)
    if not carte:
        return err[0], err[1]

    data = request.get_json()
    if not data or 'plafond_paiement' not in data:
        return jsonify({'error': 'Plafond manquant'}), 400

    try:
        nouveau_plafond = float(data['plafond_paiement'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Format de plafond invalide'}), 400

    if nouveau_plafond < 0:
        return jsonify({'error': 'Le plafond doit être positif'}), 400

    carte.plafond = nouveau_plafond
    db.session.commit()
    return jsonify({'message': 'Plafond mis à jour', 'plafond': nouveau_plafond}), 200


@api.route('/cartes/<int:carte_id>/paiement-en-ligne', methods=['PATCH'])
@jwt_required()
def toggle_paiement_en_ligne(carte_id):
    carte, *err = _verify_carte_ownership(carte_id)
    if not carte:
        return err[0], err[1]

    data = request.get_json()
    if 'active' not in data:
        return jsonify({'erreur': 'Champ "active" requis'}), 400

    carte, error = CarteController.set_paiment_en_ligne(carte_id, bool(data['active']))
    if error:
        return jsonify({'error': error}), 500

    return jsonify({'success': True, 'message': 'Paiement en ligne mis à jour'}), 200


@api.route('/cartes/<int:carte_id>/paiement-sans-contact', methods=['PATCH'])
@jwt_required()
def toggle_paiement_sans_contact(carte_id):
    carte, *err = _verify_carte_ownership(carte_id)
    if not carte:
        return err[0], err[1]

    data = request.get_json()
    if 'active' not in data:
        return jsonify({'erreur': 'Champ "active" requis'}), 400

    carte, error = CarteController.set_paiment_sans_contact(carte_id, bool(data['active']))
    if error:
        return jsonify({'erreur': error}), 500

    return jsonify({'success': True, 'message': 'Paiement sans contact mis à jour'}), 200
