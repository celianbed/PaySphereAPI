from app import db

class TypeCompte(db.Model):
    __tablename__ = 'type_compte'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)

    comptes = db.relationship("Compte", back_populates="type_compte", cascade="all, delete")

    def to_dict(self):
        return {
            'id' : self.id,
            'nom' : self.nom,
        }
    def set_nom(self, nom):
        self.nom = nom

    def set_id(self, id):
        self.id = id

    def get_nom(self):
        return self.nom

    def get_id(self):
        return self.id