from app.models.TypeCompte import TypeCompte


class TypeCompteController:

    @staticmethod
    def create_TypeCompte(type_compte_id:int,nom:str) -> TypeCompte:

        return TypeCompte(
            id=type_compte_id,
            nom=nom
        )

    @staticmethod
    def get_type_compte_by_id(type_compte_id:int) -> TypeCompte:
        return TypeCompte.query.get(type_compte_id)
