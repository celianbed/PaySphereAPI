from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .models import Authentification, Carte, Client,Compte,NotificationsClients,Notification,Pret,Rib,Statut,Transaction,TypeCompte,User,Virement,TypeCarte,TypeVirement,TypeTransaction

    with app.app_context():
        db.create_all()

    from app.models.Authentification import bcrypt
    bcrypt.init_app(app)

    from app.routes.user_route import api
    app.register_blueprint(api, url_prefix='/PaySphereAPI')


    return app
    
  
