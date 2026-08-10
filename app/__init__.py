import os
from datetime import timedelta

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config, valider_configuration

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per hour"])

#: Chemins accessibles sans clé API : sonde de supervision et documentation.
CHEMINS_PUBLICS = ('/swagger', '/static', '/PaySphereAPI/health')

#: En-têtes de sécurité ajoutés à chaque réponse.
EN_TETES_SECURITE = {
    # Empêche le navigateur de deviner un type MIME différent de celui annoncé.
    'X-Content-Type-Options': 'nosniff',
    # L'API ne sert aucune page destinée à être affichée dans un cadre.
    'X-Frame-Options': 'DENY',
    # Aucune ressource externe n'est légitime dans une réponse d'API.
    'Content-Security-Policy': "default-src 'none'; frame-ancestors 'none'",
    # Ne pas divulguer l'URL de l'API dans le Referer des requêtes sortantes.
    'Referrer-Policy': 'no-referrer',
    # Impose HTTPS pendant deux ans pour les clients qui respectent HSTS.
    'Strict-Transport-Security': 'max-age=63072000; includeSubDomains',
}


def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(config_class or Config)

    if not app.config.get('TESTING'):
        valider_configuration(app.config)

    # Render et Cloudflare placent l'API derrière un proxy : sans ce correctif,
    # `get_remote_address` retourne l'adresse du proxy et la limitation de débit
    # applique un unique quota partagé par l'ensemble des utilisateurs.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    # JWT_ACCESS_HOURS / JWT_REFRESH_DAYS étaient définis dans la configuration
    # mais jamais lus : les durées restaient figées à 1 heure et 7 jours.
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=app.config.get('JWT_ACCESS_HOURS', 1))
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=app.config.get('JWT_REFRESH_DAYS', 7))

    # Par défaut aucune origine n'est autorisée : une API bancaire ne doit pas
    # être appelable depuis n'importe quel site. Les origines légitimes sont
    # déclarées explicitement dans ALLOWED_ORIGINS.
    origines = [o.strip() for o in os.environ.get('ALLOWED_ORIGINS', '').split(',') if o.strip()]
    if origines:
        CORS(app, origins=origines)

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
        if request.path.startswith(CHEMINS_PUBLICS):
            return
        if api_key and request.headers.get('X-API-Key') != api_key:
            return jsonify({"erreur": "Clé API invalide ou manquante"}), 401

    @app.after_request
    def ajouter_en_tetes_securite(response):
        for nom, valeur in EN_TETES_SECURITE.items():
            response.headers.setdefault(nom, valeur)
        return response

    from .models import Authentification, Carte, Client, Compte, NotificationsClients, Notification, Pret, Rib, Statut, Transaction, TypeCompte, User, Virement, TypeCarte, TypeVirement, TypeTransaction, Beneficiaire
    from .models.TokenBlacklist import TokenBlacklist

    Migrate(app, db)

    # Le schéma est créé et versionné par Alembic (`flask db upgrade`).
    # `db.create_all()` créait silencieusement les tables manquantes au
    # démarrage, ce qui faisait diverger la base réelle des migrations.

    from app.routes import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix='/PaySphereAPI')
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    return app
