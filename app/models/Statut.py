from app import db

class Statut(db.Model):

    __tablename__ = 'statut'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20), nullable=False, unique=True)
    virements = db.relationship('Virement', backref='statut', lazy=True)

    def __init__(self, id,nom, virements):
        self.id = id
        self.nom = nom
        self.virements = virements

    def __repr__(self):
        return f'<Statut {self.nom}>'

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "virements": self.virements
        }



