from sqlalchemy.exc import SQLAlchemyError
from app.controllers.statut_controller import StatutController
from app.controllers.type_compte_controller import TypeCompteController
from app.controllers.rib_controller import RibController
from app.models.Beneficiaire import Beneficiaire
from app.models.Client import Client
from app.models.Compte import Compte
from app.models.Rib import Rib
from app.models.User import User
from app import db

class CompteController:

    @staticmethod
    def get_all_comptes():
        return Compte.query.all()

    @staticmethod
    def get_compte_by_id(compte_id):
        return Compte.query.get(compte_id)

    @staticmethod
    def get_compte_by_iban(iban):
        return Compte.query.join(Rib).filter(Rib.iban == iban).first()

    @staticmethod
    def create_compte(client:Client):

        compte = Compte(
            client = client,
            type_compte=TypeCompteController.get_type_compte_by_id(1),
            statut= StatutController.get_statut_by_id(3),
        )

        db.session.add(compte)
        db.session.commit()

        RibController.create_rib(compte,client)

        return compte

    @staticmethod
    def update_compte(compte:Compte, data):
        try:
            for key, value in data.items():
                setattr(compte, key, value)
            db.session.commit()
            return compte
        except SQLAlchemyError as e:
            return None

    @staticmethod
    def delete_compte(compte: Compte):
        for virement in compte.virements_recus:
            db.session.delete(virement)
        for virement in compte.virements_envoyes:
            db.session.delete(virement)

        db.session.delete(compte)
        db.session.commit()
        return compte





