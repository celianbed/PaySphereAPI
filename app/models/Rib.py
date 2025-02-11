from app import db

class Rib(db.Model):
    rib_id = db.Column(db.Integer, primary_key=True)
    compte_id = db.Column(db.Integer, db.ForeignKey('compte.compte_id'))
    iban = db.Column(db.String(34), unique=True, nullable=False)
    bic = db.Column(db.String(11), nullable=False)
    titulaire_compte = db.Column(db.String(100), nullable=False)
    banque = db.Column(db.String(100), nullable=False)
    agence = db.Column(db.String(100), nullable=True)
    adresse_banque = db.Column(db.Text, nullable=True)


