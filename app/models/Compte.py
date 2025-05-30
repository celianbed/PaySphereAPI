import random
from datetime import datetime
from typing import Tuple
from app import db
from app.models import Rib
from app.models.Client import Client
from app.models.Statut import Statut
from app.models.TypeCompte import TypeCompte
from app.models.Virement import Virement


class Compte(db.Model):
    __tablename__ = "compte"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    type_compte_id = db.Column(db.Integer, db.ForeignKey('type_compte.id'), nullable=False)
    statut_id =  db.Column(db.Integer, db.ForeignKey('statut.id'), nullable=False)
    numero_compte = db.Column(db.Integer,nullable=False)
    solde = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    date_ouverture = db.Column(db.Date, nullable=False, default=datetime.now().date())


    client = db.relationship("Client", uselist=False, back_populates="comptes")
    transactions = db.relationship("Transaction", back_populates="compte")
    type_compte = db.relationship("TypeCompte", back_populates="comptes")
    statut = db.relationship("Statut", back_populates="comptes")
    cartes = db.relationship("Carte", back_populates="compte")
    virements_envoyes = db.relationship("Virement", foreign_keys=[Virement.compte_source_id],
                                        back_populates="compte_source")
    virements_recus = db.relationship("Virement", foreign_keys=[Virement.compte_destination_id],
                                      back_populates="compte_destination")

    rib = db.relationship("Rib",
                          back_populates="compte", uselist=False)


    def __init__(self,client:Client, type_compte:TypeCompte, statut:Statut, solde=0.00, date_ouverture=None):
        self.client = client
        self.type_compte = type_compte
        self.solde = solde
        self.date_ouverture = date_ouverture if date_ouverture else datetime.now().date()  # UTC pour cohérence
        self.statut = statut
        self.virements_envoyes = []
        self.virements_recus = []
        self.numero_compte = self.generer_num_compte()
        self.cartes = []

    def __repr__(self):
        return f'<Compte {self.id} - Client {self.client_id} - Type {self.type_compte.nom} - Solde {self.solde} - Statut {self.statut.nom}>'

    def to_dict(self, fields=None, exclude=None):
        data = {
                'id': self.id,
                'client_id': self.client.id if self.client else None,
                'type_compte_nom': self.type_compte.get_nom() if self.type_compte else None,
                'solde': float(self.solde),
                'date_ouverture': self.date_ouverture.strftime('%Y-%m-%d'),
                'statut_nom': self.statut.get_nom() if self.statut else None,
                "rib": self.rib.to_dict() if self.rib else [],
                "virements_envoye": [virement_envoye.to_dict() for virement_envoye in
                                      self.virements_envoyes] if self.virements_envoyes else [],
                "virements_recu": [virement_recu.to_dict() for virement_recu in
                                   self.virements_recus] if self.virements_recus else [],
                "numero_compte": self.numero_compte,
                "cartes" : [carte.to_dict() for carte in self.cartes] if self.cartes else [],
            }

        if fields:
            data = {key: value for key, value in data.items() if key in fields}

        if exclude:
            data = {key: value for key, value in data.items() if key not in exclude}

        return data

    def get_id(self) ->int:
        return self.id

    def get_type_compte_id(self) -> int:
        return self.type_compte_id

    def get_solde(self) -> float:
        return self.solde

    def set_solde(self, solde:float):
        self.solde = solde

    def get_date_ouverture(self) -> datetime:
        return self.date_ouverture

    def get_statut(self):
        return self.statut

    def get_rib(self) -> Rib:
        return self.rib

    def set_rib(self, rib):
        self.rib = rib

    def set_type_compte(self, type_compte):
        self.type_compte = type_compte

    def get_type_compte(self) -> TypeCompte:
        return self.type_compte

    def can_make_transfer(self, montant:float) -> Tuple[bool, str]:
        """
        Vérifie si le compte peut effectuer un virement du montant spécifié.

        :param montant: Montant du virement à vérifier.
        :return: Tuple (bool, str). True si le virement est possible, False sinon avec un message d'explication.
        """
        if self.statut is None or self.statut.get_nom().lower() != "actif":
            return False, "Le compte n'est pas actif et ne peut pas effectuer de virement."

        if montant <= 0:
            return False, "Le montant du virement doit être positif."

        if self.solde < montant:
            return False, "Solde insuffisant pour effectuer ce virement."

        return True, "Le virement peut être effectué."

    @staticmethod
    def generer_num_compte():
        num = 0
        for i in range(0,6):
            num += random.randint(0,9)

        return num





