from sqlalchemy.exc import SQLAlchemyError
from app.controllers.compte_controller import CompteController
from app.models.Client import Client
from app.models.User import User
from app import db

class ClientController:
    @staticmethod
    def get_all_clients():
        return Client.query.all()

    @staticmethod
    def get_client_by_id(client_id):
        return Client.query.get(client_id)

    @staticmethod
    def create_client(data):
        client = Client(
            client_id=data["id"],
            user_id=data["user_id"],
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

