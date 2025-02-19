from app import db


class Carte(db.Model):

    __tablename__ = 'cartes'

    id = db.Column(db.Integer, primary_key=True)
    compte_id = db.Column(db.Integer, db.ForeignKey('compte.id'))
    numero_carte = db.Column(db.String(20), unique=True, nullable=False)
    date_expiration = db.Column(db.Date, nullable=False)
    code_securite = db.Column(db.String(4), nullable=False)
    type_carte = db.Column(db.String(50), nullable=False)

    compte = db.relationship('Compte',back_populates='cartes')

    def __init__(self, numero_carte, date_expiration, code_securite, type_carte):
        self.numero_carte = numero_carte
        self.date_expiration = date_expiration
        self.code_securite = code_securite
        self.type_carte = type_carte


    def __repr__(self):
        return f'<Carte {self.numero_carte}>'


    def to_dict(self):
        return {
            "id": self.id,
            "numero_carte": self.numero_carte,
            "date_expiration": self.date_expiration,
            "code_securite": self.code_securite,
            "type_carte": self.type_carte,
        }