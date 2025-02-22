from app.controllers.authentification_controller import AuthentificationController
from app.models.Rib import Rib
from app.models.User import User
from app import db

class RibController:
        @staticmethod
        def get_all_rib():
            return Rib.query.all()

        @staticmethod
        def get_rib_by_id(user_id):
            return Rib.query.get(user_id)

        @staticmethod
        def create_rib(compte):
            iban,country_code = Rib.generate_iban()

            rib = Rib(
                compte_id=compte.id,
                iban= iban,
                bic= country_code,
                titulaire_compte=compte.client_id,
                banque="PaySphere",
                agence=None,
                adresse_banque=None,
            )
            db.session.add(rib)
            db.session.commit()

            return rib

        @staticmethod
        def update_rib(user, data):
            try:
                for key, value in data.items():
                    setattr(user, key, value)
                db.session.commit()
                return user
            except:
                return None

