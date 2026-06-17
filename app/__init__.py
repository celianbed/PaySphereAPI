import os
from datetime import timedelta

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

from config import Config

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per hour"])


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

    allowed_origins = os.environ.get('ALLOWED_ORIGINS', '*').split(',')
    CORS(app, origins=allowed_origins)

    limiter.init_app(app)

    SWAGGER_URL = "/swagger"
    API_URL = "/static/swagger.json"

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'PaySphereAPI',
        }
    )

    from app.routes import jwt, mail, bcrypt
    jwt.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)

    api_key = os.environ.get('API_KEY')

    @app.before_request
    def check_api_key():
        if request.path.startswith('/swagger') or request.path.startswith('/static'):
            return
        if api_key and request.headers.get('X-API-Key') != api_key:
            return jsonify({"erreur": "Clé API invalide ou manquante"}), 401

    from .models import Authentification, Carte, Client, Compte, NotificationsClients, Notification, Pret, Rib, Statut, Transaction, TypeCompte, User, Virement, TypeCarte, TypeVirement, TypeTransaction, Beneficiaire
    from .models.TokenBlacklist import TokenBlacklist

    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    from app.routes import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix='/PaySphereAPI')
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    return app
