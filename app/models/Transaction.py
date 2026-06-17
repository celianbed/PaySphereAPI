from datetime import datetime
from app import db


class Transaction(db.Model):

    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    compte_id = db.Column(db.Integer, db.ForeignKey('compte.id'))
    montant = db.Column(db.Numeric(15, 2), nullable=False)
    statut_id = db.Column(db.Integer, db.ForeignKey('statut.id'))
    date_transaction = db.Column(db.DateTime, nullable=False)
    type_transaction_id = db.Column(db.Integer(), db.ForeignKey("type_transaction.id"), nullable=False)
    description = db.Column(db.Text, nullable=False)
    compte_destinataire = db.Column(db.Integer, nullable=False)

    compte = db.relationship("Compte", back_populates="transactions")
    statut = db.relationship("Statut", back_populates="transactions")
    type_transaction = db.relationship("TypeTransaction", back_populates="transactions")

    def __init__(self, compte_id, montant, statut_id, type_transaction_id, description, compte_destinataire, date_transaction=None):
        self.compte_id = compte_id
        self.montant = montant
        self.statut_id = statut_id
        self.type_transaction_id = type_transaction_id
        self.description = description
        self.compte_destinataire = compte_destinataire
        self.date_transaction = date_transaction or datetime.now()

    def __repr__(self):
        return f'<Transaction {self.id} compte={self.compte_id} montant={self.montant}>'

    def to_dict(self):
        return {
            "id": self.id,
            "compte_id": self.compte_id,
            "montant": float(self.montant),
            "statut": self.statut.to_dict() if self.statut else None,
            "date_transaction": self.date_transaction.isoformat() if self.date_transaction else None,
            "type_transaction": self.type_transaction.to_dict() if self.type_transaction else None,
            "description": self.description,
            "compte_destinataire": self.compte_destinataire,
        }
