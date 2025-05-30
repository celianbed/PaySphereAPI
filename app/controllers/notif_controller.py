from datetime import datetime
from app import db
from app.models.Notification import Notification

class NotificationController :

    @staticmethod
    def creer_notification(client_id, type_notification, message):
        notification = Notification(
            client_id=client_id,
            type_notification=type_notification,
            message=message,
            date_envoi=datetime.utcnow()
        )
        (db.session
         .add(notification))
        db.session.commit()
        return notification

    @staticmethod
    def get_notifications_by_client(client_id):
        return Notification.query.filter_by(client_id=client_id).order_by(Notification.date_envoi.desc()).all()



