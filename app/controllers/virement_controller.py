import math
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

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

        La validation du montant est faite ici et non par l'appelant : le
        contrôleur est le dernier rempart avant l'écriture en base.

        :param data: Dictionnaire contenant les détails du virement
         (``from_account``, ``to_account_iban``, ``montant``, et
         optionnellement ``type_virement`` et ``date_virement``).
        :return: Un triplet ``(effectue, message, virement)``. ``virement``
         vaut ``None`` lorsque ``effectue`` est ``False``. Le nombre de valeurs
         retournées est constant, afin que l'appelant n'ait jamais à deviner
         combien de valeurs dépaqueter.
        """
        # Validation du montant avant toute autre chose : une valeur non
        # numérique ne doit pas remonter en exception jusqu'à la couche HTTP.
        montant_brut = data.get('montant', 0)
        try:
            montant: float = float(montant_brut)
        except (TypeError, ValueError):
            return False, "Le montant doit être un nombre.", None

        if math.isnan(montant) or math.isinf(montant):
            return False, "Le montant doit être un nombre fini.", None

        # Récupération des comptes
        compte_source: Compte = CompteController.get_compte_by_id(data.get('from_account'))
        compte_dest: Compte = CompteController.get_compte_by_iban(data.get('to_account_iban'))

        # Vérifications de base
        if not compte_source:
            return False, "Compte emetteur non trouvé.", None

        if not compte_dest:
            return False, "Compte recepteur non trouvée", None

        if compte_source.get_id() == compte_dest.get_id():
            return False, "Le compte émetteur et le compte destinataire sont identiques.", None

        if montant <= 0:
            return False, "Le montant du transfert dois être supérieur à 0€ ", None

        # Vérification de la possibilité du virement
        peut_virement, message = compte_source.can_make_transfer(montant)
        if not peut_virement:
            return False, message, None

        try:
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
                type_virement=TypeVirementController.get_type_virement_by_id(data.get('type_virement', 1)),
            )

            db.session.add(virement)

            # commit=False : les soldes, le virement et la notification doivent
            # être validés en une seule transaction, sinon un échec en fin de
            # parcours laisserait les soldes modifiés sans trace du virement.
            NotificationController.creer_notification(
                client_id=compte_dest.client.id,
                type_notification="virement_recu",
                message=f"Vous avez reçu {montant:.2f} € de {compte_source.client.prenom} {compte_source.client.nom}",
                commit=False,
            )

            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return False, "Le virement n'a pas pu être enregistré.", None

        return True, message, virement

    @staticmethod
    def get_all_virements():
        return Virement.query.all()

    @staticmethod
    def get_virements_by_client(client_id):
        """
        Retourne les virements émis ou reçus par les comptes d'un client.

        Utilisé par ``GET /virement`` pour ne jamais exposer les mouvements
        d'un autre client.

        :param client_id: Identifiant du client concerné.
        :return: Liste de virements, du plus récent au plus ancien.
        """
        comptes_ids = [
            compte_id
            for (compte_id,) in db.session.query(Compte.id).filter(Compte.client_id == client_id).all()
        ]
        if not comptes_ids:
            return []

        return (Virement.query
                .filter(db.or_(Virement.compte_source_id.in_(comptes_ids),
                               Virement.compte_destination_id.in_(comptes_ids)))
                .order_by(Virement.date_virement.desc(), Virement.id.desc())
                .all())

    @staticmethod
    def verifier_beneficiaire_existant(to_account_iban):
        """
        Vérifie si un bénéficiaire (compte) existe via son IBAN.
        :param to_account_iban: L'IBAN à vérifier
        :return: True si le bénéficiaire existe, sinon False
        """
        compte_dest = CompteController.get_compte_by_iban(to_account_iban)
        return compte_dest is not None
