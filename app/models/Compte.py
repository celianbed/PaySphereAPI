from app import db

class Compte(db.Model):
    compte_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    type_compte = db.Column(db.String(50), nullable=False)
    solde = db.Column(db.Numeric(15,2), nullable=False)
    date_ouverture = db.Column(db.Date, nullable=False)
    statut = db.Column(db.String(20), nullable=False)
