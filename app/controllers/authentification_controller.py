from app import db
from app.models.Authentification import Authentification
from app.models.User import User


class AuthentificationController:

    @staticmethod
    def authenticate_user(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def create_auth(password,user):
        auth = Authentification(
            user_id=user.id,
            password=password,
            derniere_connexion=None
        )

        db.session.add(auth)
        db.session.commit()

        return auth



