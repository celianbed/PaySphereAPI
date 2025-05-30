from app.models.Authentification import Authentification
from app.models.User import User
from app import db

class AuthentificationController:

    @staticmethod
    def authenticate_user(username:str, password:str)-> User | None:
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def create_auth(password,user):
        auth = Authentification(
            user=user,
            password=password,
            derniere_connexion=None
        )

        db.session.add(auth)
        db.session.commit()

        return auth


    @staticmethod
    def get_auth_by_user_id(user_id):
        return Authentification.query.filter_by(user_id=user_id).first()





