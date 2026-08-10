from datetime import datetime
from app import db
from app.models.Notification import Notification

class NotificationController :

    @staticmethod
    def creer_notification(client_id, type_notification, message, commit=True):
        """
        Crée une notification pour un client.

        :param commit: valider immédiatement la transaction. Les appelants qui
         inscrivent la notification dans une opération plus large (un virement,
         par exemple) passent ``False`` afin que l'ensemble soit validé ou
         annulé d'un bloc.
        :return: la notification créée.
        """
        notification = Notification(
            client_id=client_id,
            type_notification=type_notification,
            message=message,
            date_envoi=datetime.utcnow()
        )
        db.session.add(notification)
        if commit:
            db.session.commit()
        return notification

    @staticmethod
    def get_notifications_by_client(client_id):
        return Notification.query.filter_by(client_id=client_id).order_by(Notification.date_envoi.desc()).all()



