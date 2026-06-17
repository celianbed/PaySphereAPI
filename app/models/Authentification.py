import datetime
from app import db


class Authentification(db.Model):

    __tablename__ = 'authentification'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    password_hash = db.Column(db.String(255), nullable=False)
    derniere_mise_a_jour = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship("User", back_populates="authentification")

    def __init__(self, user, password, derniere_connexion=None):
        self.user = user
        self.set_password(password)
        self.derniere_mise_a_jour = derniere_connexion

    def __repr__(self) -> str:
        return f'<Authentification {self.user.get_id()} {self.password_hash}>'

    def to_dict(self, fields=None) -> dict:
        data = {
            "user_id": self.user.get_id(),
            "derniere_connexion": self.derniere_mise_a_jour.isoformat() if self.derniere_mise_a_jour else None,
        }

        if not fields:
            return data

        return {key: value for key, value in data.items() if key in fields}

    def _get_bcrypt(self):
        from app.routes.api import bcrypt
        return bcrypt

    def set_password(self, password: str):
        bcrypt = self._get_bcrypt()
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def is_password_valid(self, password: str):
        bcrypt = self._get_bcrypt()
        return bcrypt.check_password_hash(self.password_hash, password)
