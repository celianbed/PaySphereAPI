from app import db


class Authentification(db.Model):
    __tablename__ = 'authentification' 

    nom = db.Column(db.String(50),primary_key=True,nullable=False)
    prenom  = db.Column(db.String(50),nullable=False)

