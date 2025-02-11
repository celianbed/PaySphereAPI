from app import db


class Carte(db.Model):
    carte_id = db.Column(db.Integer, primary_key=True)
    compte_id = db.Column(db.Integer, db.ForeignKey('compte.compte_id'))
    numero_carte = db.Column(db.String(20), unique=True, nullable=False)
    date_expiration = db.Column(db.Date, nullable=False)
    code_securite = db.Column(db.String(4), nullable=False)
    type_carte = db.Column(db.String(50), nullable=False)