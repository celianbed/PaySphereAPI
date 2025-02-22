from app import db


class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    type_notification = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_envoi = db.Column(db.DateTime, nullable=False)

    clients = db.relationship("Client", secondary="notification_clients", back_populates="notifications")


    def __init__(self, client_id, type_notification, message, date_envoi):
        self.client_id = client_id
        self.type_notification = type_notification
        self.message = message
        self.date_envoi = date_envoi

    def __repr__(self):
        return f'<Notification {self.id} {self.client_id} {self.type_notification} {self.message} {self.date_envoi}>'


    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "type_notification": self.type_notification,
            "message": self.message,
            "date_envoi": self.date_envoi,
        }