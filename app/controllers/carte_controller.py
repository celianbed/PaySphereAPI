from datetime import datetime, timedelta
from flask_mail import Message
from app.models.Carte import Carte
from app import db
from app.models.Transaction import Transaction
from app.routes import mail


class CarteController:
    @staticmethod
    def opposer_carte(carte_id):
        carte = Carte.query.get(carte_id)
        if not carte:
            return None
        carte.active = False
        db.session.commit()
        return carte

    @staticmethod
    def set_paiment_sans_contact(carte_id: int, active: bool):
        carte = Carte.query.get(carte_id)
        if not carte:
            return None, "Carte introuvable"

        carte.paiment_sans_contact = active
        try:
            db.session.commit()
            return carte, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def set_paiment_en_ligne(carte_id: int, active: bool):
        carte = Carte.query.get(carte_id)
        if not carte:
            return None, "Carte introuvable"

        carte.paiment_en_ligne = active
        try:
            db.session.commit()
            return carte, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def envoyer_mail():
        message = "Ceci est un test avec é à ù"
        print("Type du message :", type(message))
        print("Valeur du message :", message)
        msg = Message(
            subject="Test",
            recipients=["celianbedminster@proton.me"],
            body=message,
            charset = 'utf-8'
        )
        mail.send(msg)




    @staticmethod
    def get_carte_by_id(carte_id):
        return Carte.query.get(carte_id)


    @staticmethod
    def calculer_utilisation_plafond(carte_id):
        aujourd_hui = datetime.now()
        limite = aujourd_hui - timedelta(days=30)
        carte = CarteController.get_carte_by_id(carte_id)
        compte_id = carte.compte_id

        total_depense = db.session.query(db.func.sum(Transaction.montant)) \
                            .filter(Transaction.compte_id == compte_id) \
                            .filter(Transaction.date_virement >= limite) \
                            .scalar() or 0.0

        reste = max(carte.plafond - total_depense, 0.0)
        pourcentage = min(total_depense / carte.plafond, 1.0)

        return round(total_depense, 2), round(reste, 2), round(pourcentage * 100, 2)



