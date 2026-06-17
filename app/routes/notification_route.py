from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.controllers.notif_controller import NotificationController
from app.models.Notification import Notification
from app.routes import api


@api.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    current_user_id = int(get_jwt_identity())
    from app.controllers.user_controller import UserController
    user = UserController.get_user_by_id(current_user_id)
    if not user or not user.client:
        return jsonify([]), 200

    notifs = NotificationController.get_notifications_by_client(user.client.id)
    return jsonify([n.to_dict() for n in notifs]), 200


@api.route('/notifications/<int:notif_id>/lu', methods=['POST'])
@jwt_required()
def marquer_notif_vue(notif_id):
    current_user_id = int(get_jwt_identity())
    notif = Notification.query.get(notif_id)

    if not notif:
        return jsonify({"error": "Notification non trouvée"}), 404

    from app.controllers.user_controller import UserController
    user = UserController.get_user_by_id(current_user_id)
    if not user or not user.client or notif.client_id != user.client.id:
        return jsonify({"error": "Accès interdit"}), 403

    notif.vu = True
    db.session.commit()
    return jsonify({"message": "Notification marquée comme lue"}), 200
