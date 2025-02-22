from sqlalchemy.exc import SQLAlchemyError

from app.controllers.rib_controller import RibController
from app.models.Compte import Compte
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
    def create_compte(data):
        compte = Compte(
            client_id=data["client_id"],
            type_compte=data["type_compte"],
            solde=data["solde"],
            date_ouverture=data["date_ouverture"],
            statut=data["statut"]
        )

        RibController.create_rib(data["compte_id"])

        db.session.add(compte)
        db.session.commit()
        return compte

    @staticmethod
    def update_compte(compte, data):
        try:
            for key, value in data.items():
                setattr(compte, key, value)
            db.session.commit()
            return compte
        except SQLAlchemyError as e:
            return None

    @staticmethod
    def delete_compte(compte: Compte) -> User:
        db.session.delete(compte.virements_recus)
        db.session.commit()

        db.session.delete(compte.virements_transfere)
        db.session.commit()

        db.session.delete(compte)
        db.session.commit()
        return compte


