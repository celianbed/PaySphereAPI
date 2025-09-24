from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    SWAGGER_URL = "/swagger"
    API_URL = "/static/swagger.json"

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'PaySphereAPI',
        }
    )

    from app.routes import jwt,mail,bcrypt
    jwt.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)


    from .models import Authentification, Carte, Client,Compte,NotificationsClients,Notification,Pret,Rib,Statut,Transaction,TypeCompte,User,Virement,TypeCarte,TypeVirement,TypeTransaction,Beneficiaire

    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()


    from app.routes import api

    print("=== Vérification des fonctions différées dans le blueprint ===")
    for rule in api.deferred_functions:
        try:
            fn = rule.__closure__[0].cell_contents
            print("Route enregistrée :", getattr(fn, '__name__', str(fn)))
        except Exception:
            print("Route: inconnue")

    app.register_blueprint(api, url_prefix='/PaySphereAPI')
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)




    return app
    
  
