from app import db

class Authentification(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    mot_de_passe_hash = db.Column(db.String(255), nullable=False)
    derniere_connexion = db.Column(db.DateTime, nullable=True)