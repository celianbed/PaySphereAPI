from app import db
from datetime import datetime
import re

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nom = db.Column(db.String(255), nullable=False)
    prenom = db.Column(db.String(255), nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    username = db.Column(db.Text, unique=True, nullable=False)
    date_creation = db.Column(db.Date, nullable=False)
    mise_a_jour = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, default=True)

    client = db.relationship("Client", uselist=False, back_populates="user")

    def __init__(self, nom, prenom, email, username, date_creation, mise_a_jour=None, active=True):
        self.name = nom
        self.prenom = prenom
        self.email = email
        self.username = username
        self.date_creation = date_creation
        self.mise_a_jour = mise_a_jour
        self.active = active

    def __repr__(self):
        return f"<User id={self.id} nom={self.nom} prenom={self.prenom} email={self.email}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "username": self.username,
            "date_creation": self.date_creation.isoformat(),  # Convertit la date en chaîne ISO
            "mise_a_jour": self.mise_a_jour.isoformat() if self.mise_a_jour else None,  # Vérification si mise_a_jour existe
            "active": self.active
        }

    def is_active(self):
        return self.active

    def full_name(self):
        return f"{self.prenom} {self.nom}"

    def last_login_time(self):
        if not self.mise_a_jour:
            return "Jamais connecté"
        delta = datetime.now() - self.mise_a_jour
        return str(delta.days) + " jours" if delta.days > 0 else f"{delta.seconds // 3600} heures"

    def is_email_valid(self):
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", self.email))

    def toggle_activation(self):
        self.active = not self.active

    def get_profile_url(self):
        return f"/user/{self.id}/profile"
