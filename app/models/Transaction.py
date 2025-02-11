from app import db

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    compte_id = db.Column(db.Integer, db.ForeignKey('compte.compte_id'))
    montant = db.Column(db.Numeric(15,2), nullable=False)
    date_transaction = db.Column(db.DateTime, nullable=False)
    type_transaction = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    compte_destinataire = db.Column(db.Integer, nullable=False)
