from app import db

class TypeCompte(db.Model):
    __tablename__ = 'type_compte'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)

    comptes = db.relationship("Compte", back_populates="type_compte", cascade="all, delete")