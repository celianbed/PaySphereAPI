from app import db
from app.models.Client import Client


class Beneficiaire(db.Model):

    __tablename__ = 'beneficiaires'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    iban = db.Column(db.String(34), unique=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

    client = db.relationship('Client', back_populates='beneficiaires')


    def __init__(self, nom:str, iban:str, client:Client):
        self.nom = nom
        self.iban = iban
        self.client = client

    def __repr__(self) -> str:
        return f'<iban {self.iban}>'


    def to_dict(self, fields=None) -> dict:
        data = {
            "id": self.id,
            "nom": self.nom,
            "iban": self.iban,
            "client_id": self.client_id,
        }

        if not fields:
            return data

        return {key: value for key, value in data.items() if key in fields}