from app import db

class TypeCarte(db.Model):
    __tablename__ = 'type_carte'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)

    cartes = db.relationship("Carte", back_populates="type_carte", cascade="all, delete")

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