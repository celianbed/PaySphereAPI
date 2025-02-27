import datetime
from app import db
from app.models import TypeCarte


class Carte(db.Model):

    __tablename__ = 'carte'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    compte_id = db.Column(db.Integer, db.ForeignKey('compte.id'),nullable=False)
    numero_carte = db.Column(db.String(20), unique=True, nullable=False)
    date_expiration = db.Column(db.Date, nullable=False)
    code_securite = db.Column(db.String(4), nullable=False)
    type_carte_id = db.Column(db.Integer,db.ForeignKey('type_carte.id'),nullable=False)

    compte = db.relationship('Compte',back_populates='cartes')
    type_carte = db.relationship('TypeCarte',back_populates='cartes')

    def __init__(self, numero_carte:int, date_expiration:datetime, code_securite:int, type_carte:TypeCarte):
        self.numero_carte = numero_carte
        self.date_expiration = date_expiration
        self.code_securite = code_securite
        self.type_carte = type_carte
        self.comptes = []


    def __repr__(self) -> str:
        return f'<Carte {self.numero_carte}>'


    def to_dict(self, fields=None) -> dict:
        data = {
            "id": self.id,
            "numero_carte": self.numero_carte,
            "date_expiration": self.date_expiration,
            "code_securite": self.code_securite,
            "type_carte": self.type_carte,
            "comptes_lié":[compte.to_dict() for compte in self.comptes] if self.comptes else []
        }

        if not fields:
            return data

        return {key: value for key, value in data.items() if key in fields}