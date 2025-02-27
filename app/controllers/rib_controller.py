from app.models.Rib import Rib
from app import db

class RibController:
        @staticmethod
        def get_all_rib():
            return Rib.query.all()

        @staticmethod
        def get_rib_by_id(user_id):
            return Rib.query.get(user_id)

        @staticmethod
        def create_rib(compte,client):
            iban,country_code = Rib.generate_iban()
            rib = Rib(
                compte_id=compte.get_id(),
                iban= iban,
                bic= country_code,
                titulaire_compte= client.get_prenom() +" "+ client.get_nom(),
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

