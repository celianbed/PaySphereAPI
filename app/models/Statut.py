from app import db

class Statut(db.Model):

    __tablename__ = 'statut'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20), nullable=False, unique=True)

    virements = db.relationship('Virement', back_populates='statut')
    transactions = db.relationship('Transaction', back_populates='statut')
    comptes = db.relationship('Compte', back_populates='statut')

    def __repr__(self):
        return f'<Statut {self.nom}>'

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
        }

    def get_nom(self):
        return self.nom

    def get_id(self):
        return self.id

    def set_nom(self, nom):
        self.nom = nom

    def set_id(self, id):
        self.id = id

