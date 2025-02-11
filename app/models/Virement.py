from app import db


class Virement(db.Model):
    virement_id = db.Column(db.Integer, primary_key=True)
    compte_source_id = db.Column(db.Integer, db.ForeignKey('compte.compte_id'))
    compte_destination_id = db.Column(db.Integer, db.ForeignKey('compte.compte_id'))
    montant = db.Column(db.Numeric(15,2), nullable=False)
    date_virement = db.Column(db.DateTime, nullable=False)
    statut = db.Column(db.String(20), nullable=False)