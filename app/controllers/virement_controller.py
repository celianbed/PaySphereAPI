from datetime import datetime
from app import db
from app.controllers.compte_controller import CompteController
from app.controllers.notif_controller import NotificationController
from app.controllers.statut_controller import StatutController
from app.controllers.type_virement_controller import TypeVirementController
from app.models.Compte import Compte
from app.models.Virement import Virement


class VirementController :

    @staticmethod
    def create_virement(data):
        """
        Crée un virement bancaire entre deux comptes si possible.

        :param data: Dictionnaire contenant les détails du virement.
        :return: Objet Virement si réussi, ou un message d’erreur.
        """
        # Récupération des comptes

        compte_source: Compte = CompteController.get_compte_by_id(data.get('from_account'))
        compte_dest: Compte = CompteController.get_compte_by_iban(data.get('to_account_iban'))
        montant: float = float(data.get('montant', 0))

        # Vérifications de base
        if not compte_source:
            return False, "Compte emetteur non trouvé."

        if not compte_dest:
            return False, "Compte recepteur non trouvée"

        if montant <= 0:
            return False, "Le montant du transfert dois être supérieur à 0€ "

        # Vérification de la possibilité du virement
        peut_virement, message = compte_source.can_make_transfer(montant)
        if not peut_virement:
            return False, message

        # Mise à jour des soldes
        compte_source.set_solde(float(compte_source.get_solde()) - montant)
        compte_dest.set_solde(float(compte_dest.get_solde()) + montant)

        # Création et retour du virement
        virement = Virement(
            compte_source=compte_source,
            compte_destination=compte_dest,
            montant=montant,
            date_virement=data.get('date_virement', datetime.now().date()),
            statut=StatutController.get_statut_by_id(2),
            type_virement=TypeVirementController.get_type_virement_by_id(data.get('type_virement',1)),
        )

        db.session.add(virement)


        NotificationController.creer_notification(
            client_id=compte_source.client.id,
            type_notification="virement_envoye",
            message=f"Virement de {montant:.2f} € envoyé à {compte_dest.client.prenom} {compte_dest.client.nom}"
        )

        NotificationController.creer_notification(
            client_id=compte_dest.client.id,
            type_notification="virement_recu",
            message=f"Vous avez reçu {montant:.2f} € de {compte_source.client.prenom} {compte_source.client.nom}"
        )

        db.session.commit()

        return True, message, virement



    @staticmethod
    def get_all_virements():
        return Virement.query.all()

    @staticmethod
    def verifier_beneficiaire_existant(to_account_iban):
        """
        Vérifie si un bénéficiaire (compte) existe via son IBAN.
        :param to_account_iban: L'IBAN à vérifier
        :return: True si le bénéficiaire existe, sinon False
        """
        compte_dest = CompteController.get_compte_by_iban(to_account_iban)
        return compte_dest is not None


