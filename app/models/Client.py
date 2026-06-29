import datetime
from app import db


class Client(db.Model):

    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    num_client = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    adresse = db.Column(db.Text, nullable=False)
    numero_de_telephone = db.Column(db.String(20), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)


    comptes = db.relationship("Compte", back_populates="client")
    notifications = db.relationship("Notification",secondary="notification_clients", back_populates="client")
    prets = db.relationship("Pret", back_populates="client")
    user = db.relationship("User", back_populates="client")
    beneficiaires = db.relationship('Beneficiaire', back_populates='client', cascade='all, delete-orphan')


    def __init__(self, id, user, num_client, nom, prenom, email, adresse, numero_de_telephone, date_naissance):
        self.id = id
        self.user = user
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.adresse = adresse
        self.numero_de_telephone = numero_de_telephone
        self.date_naissance = date_naissance
        self.comptes = []
        self.num_client = num_client


    def __repr__(self):
        return f'<Client {self.id}> {self.nom} {self.prenom} {self.email} {self.adresse}'

    def to_dict(self,fields=None):
        data= {
            "client_id": self.id,
            "user_id": self.user.get_id(),
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "adresse": self.adresse,
            "numero_de_telephone": self.numero_de_telephone,
            "date_naissance": self.date_naissance.strftime("%Y-%m-%d"),
            "num_client": self.num_client,
            "comptes": [compte.to_dict() for compte in self.comptes] if self.comptes else [],
            "beneficiaires": [beneficiaire.to_dict() for beneficiaire in self.beneficiaires] if self.beneficiaires else [],
        }

        if not fields:
            return data

        return {key: value for key, value in data.items() if key in fields}

    def get_nom(self):
        return self.nom
    def get_prenom(self):
        return self.prenom
    def get_id(self):
        return self.id

    def get_num_client(self):
        return self.num_client

    def set_compte(self, compte):
        self.comptes.append(compte)

    def get_comptes(self):
        return self.comptes

    def get_identity(self):
        return f"M. {self.nom} {self.prenom}"