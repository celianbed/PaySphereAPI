import datetime
from app import db


class Carte(db.Model):

    __tablename__ = 'carte'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    compte_id = db.Column(db.Integer, db.ForeignKey('compte.id'),nullable=False)
    numero_carte = db.Column(db.String(20), unique=True, nullable=False)
    date_expiration = db.Column(db.Date, nullable=False)
    code_securite = db.Column(db.String(4), nullable=False)
    type_carte_id = db.Column(db.Integer,db.ForeignKey('type_carte.id'),nullable=False)
    active = db.Column(db.Boolean, nullable=True,default=True)
    plafond = db.Column(db.Integer, nullable=True,default=500)
    paiment_sans_contact = db.Column(db.Boolean, nullable=True,default=False)
    paiment_en_ligne = db.Column(db.Boolean, nullable=True,default=False)

    compte = db.relationship('Compte',back_populates='cartes')
    type_carte = db.relationship('TypeCarte',back_populates='cartes')

    def __init__(self, numero_carte, date_expiration, code_securite, type_carte):
        self.numero_carte = numero_carte
        self.date_expiration = date_expiration
        self.code_securite = code_securite
        self.type_carte = type_carte


    def __repr__(self) -> str:
        return f'<Carte {self.numero_carte}>'


    def to_dict(self, fields=None) -> dict:
        """
        Représentation de la carte destinée aux réponses de l'API.

        Le cryptogramme visuel (``code_securite``) est volontairement absent :
        la norme PCI-DSS interdit de le restituer, et aucun écran de
        l'application ne l'affiche.
        """
        data = {
            "id": self.id,
            "numero_carte": self.numero_carte,
            "date_expiration": self.date_expiration,
            "type_carte": self.type_carte.to_dict(),
            "numero_compte" : self.compte.numero_compte,
            "active": self.active,
            "plafond": self.plafond,
            "paiment_sans_contact": self.paiment_sans_contact,
            "paiment_en_ligne": self.paiment_en_ligne,
        }
        if not fields:
            return data

        return {key: value for key, value in data.items() if key in fields}