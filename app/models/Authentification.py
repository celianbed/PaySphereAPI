import datetime
from app import db
from flask_bcrypt import Bcrypt
from app.models import User

bcrypt = Bcrypt()

class Authentification(db.Model):

    __tablename__ = 'authentification'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    password_hash = db.Column(db.String(255), nullable=False)
    derniere_mise_a_jour = db.Column(db.DateTime,default=datetime.date.today())

    user = db.relationship("User", back_populates="authentification")


    def __init__(self, user:User,password,derniere_connexion:datetime):
        self.user:int = user
        self.set_password(password)
        self.derniere_mise_a_jour:datetime = derniere_connexion


    def __repr__(self) -> str:
        return f'<Authentification {self.user.get_id()} {self.password_hash}>'


    def to_dict(self,fields=None) -> dict:
        data = {
            "user_id": self.user.get_id(),
            "mot_de_passe_hash": self.password_hash,
            "derniere_connexion": self.derniere_mise_a_jour,
        }

        if not fields:
            return data

        return {key: value for key, value in data.items() if key in fields}

    def set_password(self, password:str) :
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')


    def is_password_valid(self, password:str) :
        return bcrypt.check_password_hash(self.password_hash, password)
