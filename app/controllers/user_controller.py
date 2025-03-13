from click import Tuple
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from app.controllers.authentification_controller import AuthentificationController
from app.models import Authentification
from app.models.User import User
from app import db

class UserController:

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_username( username):
        return User.query.filter_by(username=username).first()  # Retourne None si aucun utilisateur n'est trouvé

    @staticmethod
    def get_user_by_client_id(client_id):
        return User.client.query.filter_by(id=client_id).first()
    @staticmethod
    def create_user(data):
        try:
            user = User(
                id=data["id"],
                nom=data["nom"],
                prenom=data["prenom"],
                email=data["email"],
                username=data["username"],
                active=False
            )
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            return False,False

        auth = AuthentificationController.create_auth(data["password"],user)
        return user,auth

    @staticmethod
    def update_user(user, data):
        try:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            return e

    @staticmethod
    def delete_user(user:User) -> User:
            db.session.delete(user.authentification)
            db.session.delete(user)
            db.session.commit()
            return user


    @staticmethod
    def toggle_user(user):
        user.active = not user.active
        db.session.commit()

    @staticmethod
    def is_exist_username(user) -> bool:
        return db.session.query.get(user.username) is not None

    @staticmethod
    def is_exist_phone_number(user) -> bool:
        user.client