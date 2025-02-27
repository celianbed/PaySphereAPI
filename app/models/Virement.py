from sqlalchemy import DateTime
from app import db
from app.models import Statut
from ..models import Compte


class Virement(db.Model):

    __tablename__ = 'virement'

    id = db.Column(db.Integer, primary_key=True)
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


    def __init__(self, id, compte_source:Compte, compte_destination:Compte, montant, date_virement, statut:Statut):
        self.id = id
        self.compte_source = compte_source
        self.compte_destination = compte_destination
        self.montant = montant
        self.date_virement = date_virement
        self.statut = statut

    def __repr__(self):
        return f'<Virement {self.id} de {self.compte_source_id} à {self.compte_destination_id}>'


    def to_dict(self,fields=None):
        data= {
            "id": self.id,
            "compte_source_id": self.compte_source.get_id(),
            "compte_destination_id": self.compte_destination.get_id(),
            "montant": self.montant,
            "date_virement": self.date_virement,
            "statut": self.statut if self.statut.is_active else [],
        }

        if not fields:
            return data

        return {key: value for key, value in data.items() if key in fields}
