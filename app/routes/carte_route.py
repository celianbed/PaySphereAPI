from flask import jsonify, request
from flask_jwt_extended import jwt_required
from .api import api
from .. import db
from ..controllers.carte_controller import CarteController

from ..models.Carte import Carte


@api.route('/cartes/<int:carte_id>/opposee', methods=['POST'])
@jwt_required()
def opposer_carte(carte_id):
    carte = CarteController.get_carte_by_id(carte_id)
    if not carte:
        return jsonify({'error': 'Carte introuvable'}), 404

    carte.active = False
    db.session.commit()

    return jsonify({'success': True, 'carte': carte.to_dict()}), 200


@api.route('/cartes/<int:carte_id>/plafond', methods=['GET'])
@jwt_required()
def get_utilisation_plafond(carte_id):
    try:
        totale_depense, reste, pourcentage = CarteController.calculer_utilisation_plafond(carte_id)

        return jsonify({
            'total_utilise': round(float(totale_depense), 2),
            'reste': round(float(reste), 2),
            'pourcentage': round(float(pourcentage), 2)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/cartes/<int:carte_id>/plafond', methods=['PATCH'])
@jwt_required()
def set_plafond(carte_id):
    data = request.get_json()

    if not data or 'plafond_paiement' not in data:
        return jsonify({'error': 'Plafond manquant'}), 400

    try:
        nouveau_plafond = float(data['plafond_paiement'])

        print(nouveau_plafond)

        if nouveau_plafond < 0:
            return jsonify({'error': 'Le plafond doit être positif'}), 400

        carte = Carte.query.get(carte_id)

        if not carte:
            return jsonify({'error': 'Carte introuvable'}), 404

        carte.plafond = nouveau_plafond
        db.session.commit()

        return jsonify({'message': 'Plafond mis à jour avec succès', 'plafond': nouveau_plafond}), 200

    except ValueError:
        return jsonify({'error': 'Format de plafond invalide'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@api.route('/cartes/<int:carte_id>/paiement-en-ligne', methods=['PATCH'])
@jwt_required()
def toggle_paiement_en_ligne(carte_id):
    data = request.get_json()
    if 'active' not in data:
        return jsonify({'erreur': 'Champ "active" requis'}), 400

    carte, error = CarteController.set_paiment_sans_contact(carte_id, bool(data['active']))
    if error:
        return jsonify({'error': error}), 404 if error == "Carte introuvable" else 500

    return jsonify({
        'success': True,
        'message': 'Option Travel mise à jour avec succès',
    }), 200

@api.route('/cartes/<int:carte_id>/paiement-sans-contact', methods=['PATCH'])
@jwt_required()
def toggle_paiement_sans_contact(carte_id):
    data = request.get_json()
    if 'active' not in data:
        return jsonify({'erreur': 'Champ "active" requis'}), 400

    carte, error = CarteController.set_paiment_en_ligne(carte_id, bool(data['active']))
    if error:
        return jsonify({'erreur': error}), 404 if error == "Carte introuvable" else 500

    return jsonify({
        'success': True,
        'message': 'Option Travel mise à jour avec succès',
    }), 200
