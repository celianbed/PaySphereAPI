from app import db

class Client(db.Model):

    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    adresse = db.Column(db.Text, nullable=False)
    numero_de_telephone = db.Column(db.String(20), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)

    comptes = db.relationship("Compte", back_populates="client")
    notifications = db.relationship("Notification",secondary="notification_clients", back_populates="clients")
    prets = db.relationship("Pret", back_populates="client")
    user = db.relationship("User", back_populates="client")

    def __init__(self, client_id, user_id, nom, prenom, email, adresse, numero_de_telephone, date_naissance):
        self.client_id = client_id
        self.user_id = user_id
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.adresse = adresse
        self.numero_de_telephone = numero_de_telephone
        self.date_naissance = date_naissance

    def __repr__(self):
        return f'<Client {self.client_id}> {self.nom} {self.prenom} {self.email} {self.adresse}'

    def to_dict(self):
        return {
            "client_id": self.client_id,
            "user_id": self.user_id,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "adresse": self.adresse,
            "numero_de_telephone": self.numero_de_telephone,
            "date_naissance": self.date_naissance,
        }

