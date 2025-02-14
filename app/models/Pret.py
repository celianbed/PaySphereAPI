from  app import db

class Pret(db.Model):

    __tablename__ = "pret"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    montant_pret = db.Column(db.Numeric(15,2), nullable=False)
    taux_interet = db.Column(db.Numeric(5,2), nullable=False)
    date_demande = db.Column(db.Date, nullable=False)
    date_echeance = db.Column(db.Date, nullable=False)
    statut = db.Column(db.String(20), nullable=False)

    client = db.relationship("Client", back_populates="prets")


    def __init__(self, client_id, montant_pret, taux_interet, date_demande, date_echeance, statut):
        self.client_id = client_id
        self.montant_pret = montant_pret
        self.taux_interet = taux_interet
        self.date_demande = date_demande
        self.date_echeance = date_echeance
        self.statut = statut

    def __repr__(self):
        return f'<Pret {self.id} {self.client_id} {self.montant_pret} {self.taux_interet} {self.date_demande} {self.date_echeance} {self.statut}>'

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "montant_pret": self.montant_pret,
            "taux_interet": self.taux_interet,
            "date_demande": self.date_demande,
            "date_echeance": self.date_echeance,
        }