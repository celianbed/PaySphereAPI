from datetime import datetime

from app.controllers.compte_controller import CompteController
from app.models.Compte import Compte
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
        compte_source: Compte = CompteController.get_compte_by_id(data.get('compte_source_id'))
        compte_dest: Compte = CompteController.get_compte_by_id(data.get('compte_destination_id'))
        montant: float = float(data.get('montant', 0))

        # Vérifications de base
        if not compte_source:
            return {"success": False, "message": "Compte emetteur non trouvé."}

        if not compte_dest:
            return {"success": False, "message": "Destination account not found."}

        if montant <= 0:
            return {"success": False, "message": "Transfer amount must be greater than zero."}

        # Vérification de la possibilité du virement
        peut_virement, message = compte_source.can_make_transfer(montant)
        if not peut_virement:
            return {"success": False, "message": message}

        # Mise à jour des soldes
        compte_source.set_solde(compte_source.get_solde() - montant)
        compte_dest.set_solde(compte_dest.get_solde() + montant)

        # Création et retour du virement
        virement = Virement(
            id=data.get('id'),
            compte_source_id=compte_source.id,
            compte_destination_id=compte_dest.id,
            montant=montant,
            date_virement=data.get('date_virement', datetime.now().date()),
            statut_id=Statut.
        )

        return {"success": True, "message": "Transfer successful.", "virement": virement}







