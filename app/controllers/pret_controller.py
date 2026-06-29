from datetime import datetime
from app import db
from app.controllers.notif_controller import NotificationController
from app.models.Pret import Pret


class PretController:

    MONTANT_MIN = 500
    MONTANT_MAX = 75000

    @staticmethod
    def _calculer_taux(duree_mois):
        if duree_mois <= 12:
            return 3.5
        elif duree_mois <= 36:
            return 4.2
        else:
            return 4.9

    @staticmethod
    def creer_pret(client, montant, duree_mois):
        if montant < PretController.MONTANT_MIN or montant > PretController.MONTANT_MAX:
            return None, f"Le montant doit être entre {PretController.MONTANT_MIN}€ et {PretController.MONTANT_MAX}€."

        if duree_mois <= 0:
            return None, "La durée doit être supérieure à 0."

        taux = PretController._calculer_taux(duree_mois)
        date_demande = datetime.now().date()
        annees, mois_restants = divmod(duree_mois, 12)
        new_year = date_demande.year + annees
        new_month = date_demande.month + mois_restants
        if new_month > 12:
            new_year += 1
            new_month -= 12
        date_echeance = date_demande.replace(year=new_year, month=new_month)

        pret = Pret(
            client_id=client.id,
            montant_pret=montant,
            taux_interet=taux,
            date_demande=date_demande,
            date_echeance=date_echeance,
            statut="en_attente",
        )

        db.session.add(pret)

        NotificationController.creer_notification(
            client_id=client.id,
            type_notification="pret_demande",
            message=f"Votre demande de prêt de {montant:.2f}€ sur {duree_mois} mois a été enregistrée.",
        )

        db.session.commit()
        return pret, None

    @staticmethod
    def get_prets_by_client(client_id):
        return Pret.query.filter_by(client_id=client_id).order_by(Pret.date_demande.desc()).all()

    @staticmethod
    def get_pret_by_id(pret_id):
        return Pret.query.get(pret_id)

    @staticmethod
    def annuler_pret(pret):
        if pret.statut != "en_attente":
            return False, "Seul un prêt en attente peut être annulé."
        pret.statut = "annule"
        db.session.commit()
        return True, "Prêt annulé."
