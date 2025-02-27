from app.models.Statut import Statut


class StatutController:

    @staticmethod
    def create_statut(statut_id,nom):

        return Statut(
            id=statut_id,
            nom=nom
        )

    @staticmethod
    def get_statut_by_id(statut_id):
       return Statut.query.get(statut_id)

