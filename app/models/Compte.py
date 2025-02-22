from datetime import datetime

from app import db
from app.models.TypeCompte import TypeCompte
from app.models.Virement import Virement  # Import pour éviter référence circulaire

class Compte(db.Model):

    __tablename__ = "compte"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    type_compte_id = db.Column(db.Integer, db.ForeignKey('type_compte.id'), nullable=False)
    solde = db.Column(db.Numeric(15,2), nullable=False)
    date_ouverture = db.Column(db.Date, nullable=False)
    statut = db.Column(db.String(20), nullable=False)


    client = db.relationship("Client", uselist=False, back_populates="comptes")
    transactions = db.relationship("Transaction", back_populates="compte")
    type_compte = db.relationship("TypeCompte", back_populates="comptes")
    cartes = db.relationship("Carte", back_populates="compte")
    virements_envoyes = db.relationship("Virement", foreign_keys=[Virement.compte_source_id],
                                        back_populates="compte_source")
    virements_recus = db.relationship("Virement", foreign_keys=[Virement.compte_destination_id],
                                      back_populates="compte_destination")

    def __init__(self, client_id, type_compte=1, solde=0, date_ouverture=None, statut=4):
        self.client_id = client_id
        self.type_compte = type_compte
        self.solde = solde
        self.date_ouverture = date_ouverture if date_ouverture else datetime.now()
        self.statut = statut


    def __repr__(self):
        return f'<Compte {self.id} {self.client_id} {self.type_compte} {self.solde} {self.date_ouverture} {self.statut}>'


    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'type_compte': self.type_compte.id,
            'solde': self.solde,
            'date_ouverture': self.date_ouverture,
            'statut': self.statut,
        }