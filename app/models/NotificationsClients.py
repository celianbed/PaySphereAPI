from app import db


class NotificationClient(db.Model):

    __tablename__ = 'notification_clients'
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), primary_key=True)
    notification_id = db.Column(db.Integer, db.ForeignKey('notification.id'), primary_key=True)
    date_reception = db.Column(db.DateTime, nullable=False, server_default=db.func.now())