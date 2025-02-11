from app import db


class Notification(db.Model):
    notification_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    type_notification = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_envoi = db.Column(db.DateTime, nullable=False)