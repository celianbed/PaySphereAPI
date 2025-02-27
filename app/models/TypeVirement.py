from app import db

class TypeVirement(db.Model):
    __tablename__ = 'type_virement'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)

    virements = db.relationship("Virement", back_populates="type_virement", cascade="all, delete")

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