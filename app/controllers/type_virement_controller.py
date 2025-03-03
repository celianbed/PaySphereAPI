from app.models.TypeVirement import TypeVirement


class TypeVirementController:

    @staticmethod
    def get_type_virement_by_id(id):
        return TypeVirement.query.get(id)