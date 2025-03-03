from datetime import datetime
from app import db
from app.controllers.compte_controller import CompteController
from app.controllers.statut_controller import StatutController
from app.models.Compte import Compte
from app.models.TypeVirement import TypeVirement
from app.models.Virement import Virement


class VirementController :

    @staticmethod
    def create_virement(data):
        """
        Creates a bank transfer (virement) between two accounts if possible.

        :param data: Dictionary containing virement details.
        :return: Virement object if successful, or an error message.
        """
        # Récupération des comptes

        compte_source: Compte = CompteController.get_compte_by_id(data.get('sender_id'))
        compte_dest: Compte = CompteController.get_compte_by_id(data.get('receiver_id'))
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
            id=data.get('id'),
            compte_source=compte_source,
            compte_destination=compte_dest,
            montant=montant,
            date_virement=data.get('date_virement', datetime.now().date()),
            statut=StatutController.get_statut_by_id(2),
            type_virement=TypeVirement.get_type_virement_by_id(data.get('type_virement',1)),
        )

        db.session.add(virement)
        db.session.commit()

        return True, message, virement






