from sqlalchemy.exc import SQLAlchemyError
from app.controllers.compte_controller import CompteController
from app.controllers.user_controller import UserController
from app.models.Beneficiaire import Beneficiaire
from app.models.Client import Client
from app.models.User import User
from app import db

class ClientController:
    @staticmethod
    def get_all_clients() ->  Client:
        return Client.query.all()

    @staticmethod
    def get_client_by_id(client_id) -> Client:
        return Client.query.get(client_id)


    @staticmethod
    def create_client(data):

        user = UserController.get_user_by_id(data['user_id'])
        client = Client(
            id=data["id"],
            user=user,
            num_client=data["num_client"],
            nom=data["nom"],
            prenom=data["prenom"],
            email=data["email"],
            adresse=data["adresse"],
            numero_de_telephone=data["numero_de_telephone"],
            date_naissance=data["date_naissance"]
        )
        db.session.add(client)
        db.session.commit()

        CompteController.create_compte(client)

        return client

    @staticmethod
    def creer_beneficiaire(iban: str, nom: str, client) -> Beneficiaire:
        new_benef = Beneficiaire(iban=iban, nom=nom, client=client)
        db.session.add(new_benef)
        db.session.commit()
        return new_benef


    @staticmethod
    def update_client(client, data):
        try:
            for key, value in data.items():
                setattr(client, key, value)
            db.session.commit()
            return client
        except SQLAlchemyError as e:
            db.session.rollback()
            return None
        except Exception as e:
            return e

    @staticmethod
    def delete_client(client:Client) -> User:
            db.session.delete()
            db.session.delete()
            db.session.commit()
            return client

    @staticmethod
    def get_client_by_numero(numero_client):
        return Client.query.filter_by(num_client=numero_client).first()

    @staticmethod
    def supprimer_beneficiaire(beneficiaire_id):
        beneficiaire =  Beneficiaire.query.get(beneficiaire_id)

        if not beneficiaire:
            return {"erreur": "Bénéficiaire introuvable"}, 404

        try:
            db.session.delete(beneficiaire)
            db.session.commit()
            return {"message": "Bénéficiaire supprimé avec succès"}, 200
        except Exception as e:
            db.session.rollback()
            return {"erreur": f"Erreur lors de la suppression : {str(e)}"}, 500





