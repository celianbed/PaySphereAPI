from sqlalchemy import DateTime
from app import db
from app.models import Statut, TypeVirement
from ..models import Compte


class Virement(db.Model):

    __tablename__ = 'virement'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    compte_source_id = db.Column(db.Integer, db.ForeignKey('compte.id'))
    compte_destination_id = db.Column(db.Integer, db.ForeignKey('compte.id'))
    montant = db.Column(db.Numeric(15,2), nullable=False)
    date_virement:DateTime = db.Column(db.DateTime, nullable=False)
    statut_id = db.Column(db.Integer, db.ForeignKey('statut.id'), nullable=False)
    type_virement_id = db.Column(db.Integer, db.ForeignKey('type_virement.id'), nullable=False)

    compte_source = db.relationship("Compte", foreign_keys=[compte_source_id], back_populates="virements_envoyes")
    compte_destination = db.relationship("Compte", foreign_keys=[compte_destination_id],back_populates="virements_recus")
    type_virement = db.relationship("TypeVirement", back_populates="virements")


    statut = db.relationship('Statut',back_populates='virements')


    def __init__(self, compte_source:Compte, compte_destination:Compte, montant, date_virement, statut:Statut,type_virement:TypeVirement):
        self.compte_source = compte_source
        self.compte_destination = compte_destination
        self.montant = montant
        self.date_virement = date_virement
        self.statut = statut
        self.type_virement = type_virement

    def __repr__(self):
        return f'<Virement {self.id} de {self.compte_source_id} à {self.compte_destination_id}>'


    def to_dict(self,fields=None):
        data= {
            "id": self.id,
            "compte_source_nom": self.compte_source.client.get_identity(),
            "compte_destination_nom": self.compte_destination.client.get_identity(),
            "montant": self.montant,
            "date_virement": self.date_virement,
            "statut_nom": self.statut.get_nom() if self.statut else None,
            "type_virement_nom": self.type_virement.get_nom() if self.type_virement else None,
        }

        if not fields:
            return data

        return {key: value for key, value in data.items() if key in fields}
