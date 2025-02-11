from app.models.User import User
from app import db
from datetime import datetime

class UserController:
    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def create_user(data):
        user = User(
            nom=data["nom"],
            prenom=data["prenom"],
            email=data["email"],
            username=data["username"],
            date_creation=datetime.now().date()
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_user(user, data):
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user):
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def toggle_user(user):
        user.active = not user.active
        db.session.commit()
