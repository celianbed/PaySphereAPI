from app import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class Authentification(db.Model):

    __tablename__ = 'authentification'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    mot_de_passe_hash = db.Column(db.String(255), nullable=False)
    derniere_connexion = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates="authentification")


    def __init__(self, user_id,password,derniere_connexion):
        self.user_id = user_id
        self.set_password(password)
        self.derniere_connexion = derniere_connexion


    def __repr__(self):
        return f'<Authentification {self.user_id} {self.mot_de_passe_hash}>'


    def to_dict(self):
        return {
            "user_id": self.user_id,
            "mot_de_passe_hash": self.mot_de_passe_hash,
            "derniere_connexion": self.derniere_connexion,
        }

    def set_password(self, password):
        self.mot_de_passe_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def is_password_valid(self, password):
        return bcrypt.check_password_hash(self.mot_de_passe_hash, password).decode('utf-8')
