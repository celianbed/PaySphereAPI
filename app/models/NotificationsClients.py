from sqlalchemy import PrimaryKeyConstraint

from app import db


class NotificationClient(db.Model):

    __tablename__ = 'notification_clients'

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    notification_id = db.Column(db.Integer, db.ForeignKey('notification.id'))
    date_reception = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    __table_args__ = (
        PrimaryKeyConstraint('client_id', 'notification_id'),
    )