from  app import db

class Pret(db.Model):
    pret_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    montant_pret = db.Column(db.Numeric(15,2), nullable=False)
    taux_interet = db.Column(db.Numeric(5,2), nullable=False)
    date_demande = db.Column(db.Date, nullable=False)
    date_echeance = db.Column(db.Date, nullable=False)
    statut = db.Column(db.String(20), nullable=False)