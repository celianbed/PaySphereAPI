from app import db

class Transaction(db.Model):

    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    compte_id = db.Column(db.Integer, db.ForeignKey('compte.id'))
    montant = db.Column(db.Numeric(15,2), nullable=False)
    statit_id= db.Column(db.Integer, db.ForeignKey('statut.id'))
    date_transaction = db.Column(db.DateTime, nullable=False)
    type_transaction = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    compte_destinataire = db.Column(db.Integer, nullable=False)

    compte = db.relationship("Compte", back_populates="transactions")
    statut = db.relationship("Statut", back_populates="transactions")

    def __init__(self, client_id, user_id, nom, prenom, email, date_naissance, statut):
        self.client_id = client_id
        self.user_id = user_id
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.date_naissance = date_naissance
        self.statut = statut

    def __repr__(self):
        return f'<Transaction {self.id} {self.client_id} {self.montant} {self.date_transaction} {self.type_transaction} {self.description} {self.compte_destinataire}>'


    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "montant": self.montant,
            "date_transaction": self.date_transaction,
            "type_transaction": self.type_transaction,
            "description": self.description,
            "compte_destinataire": self.compte_destinataire,
        }
