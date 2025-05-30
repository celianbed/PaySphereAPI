from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.controllers.notif_controller import NotificationController
from app.models.Notification import Notification
from app.routes import api


@api.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    client_id = get_jwt_identity()
    notifs = NotificationController.get_notifications_by_client(client_id)


    return jsonify([n.to_dict() for n in notifs]), 200


@api.route('/notifications/<int:notif_id>/lu', methods=['POST'])
@jwt_required()
def marquer_notif_vue(notif_id):
    notif = Notification.query.get(notif_id)
    if notif:
        db.session.delete(notif)
        db.session.commit()
        return jsonify({"message": "Notification marquée comme vue"}), 200
    return jsonify({"error": "Notification non trouvée"}), 404


