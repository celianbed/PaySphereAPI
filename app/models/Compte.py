from app import db

class Compte(db.Model):

    __tablename__ = "compte"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    type_compte_id = db.Column(db.Integer, db.ForeignKey('type_compte.id'), nullable=False)
    solde = db.Column(db.Numeric(15,2), nullable=False)
    date_ouverture = db.Column(db.Date, nullable=False)
    statut = db.Column(db.String(20), nullable=False)

    client = db.relationship("Client", uselist=False, back_populates="comptes")
    transactions = db.relationship("Transaction", back_populates="compte")
    type_compte = db.relationship("TypeCompte", back_populates="comptes")

    def __init__(self, client_id, type_compte, solde, date_ouverture, statut):
        self.client_id = client_id
        self.type_compte = type_compte
        self.solde = solde
        self.date_ouverture = date_ouverture
        self.statut = statut


    def __repr__(self):
        return f'<Compte {self.id} {self.client_id} {self.type_compte} {self.solde} {self.date_ouverture} {self.statut}>'