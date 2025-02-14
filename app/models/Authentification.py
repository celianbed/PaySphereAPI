from app import db

class Authentification(db.Model):

    __tablename__ = 'authentification'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    mot_de_passe_hash = db.Column(db.String(255), nullable=False)
    derniere_connexion = db.Column(db.DateTime, nullable=True)


    def __init__(self, user_id, client_id, mot_de_passe_hash, derniere_connexion):
        self.user_id = user_id
        self.client_id = client_id
        self.mot_de_passe_hash = mot_de_passe_hash
        self.derniere_connexion = derniere_connexion


    def __repr__(self):
        return f'<Authentification {self.user_id} {self.client_id}>'


    def to_dict(self):
        return {
            "user_id": self.user_id,
            "client_id": self.client_id,
            "mot_de_passe_hash": self.mot_de_passe_hash,
            "derniere_connexion": self.derniere_connexion,
        }