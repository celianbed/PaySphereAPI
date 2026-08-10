"""
Configuration de l'application, lue depuis l'environnement.

Aucun secret ne dispose de valeur de repli. Une clé générée à la volée au
démarrage paraît inoffensive mais produit deux pannes silencieuses en
production : chaque worker Gunicorn signe alors avec une clé différente — un
jeton émis par l'un est rejeté par l'autre — et le moindre redémarrage
invalide toutes les sessions en cours. L'application refuse donc de démarrer
si un secret manque, plutôt que de fonctionner de façon erratique.
"""

import os

from dotenv import load_dotenv

load_dotenv()

#: Variables sans lesquelles l'application ne peut pas fonctionner correctement.
VARIABLES_REQUISES = ('DATABASE_URL', 'SECRET_KEY', 'JWT_SECRET_KEY')

#: Longueur minimale acceptée pour un secret, en caractères.
LONGUEUR_MINIMALE_SECRET = 32


class ConfigurationError(RuntimeError):
    """Levée lorsqu'une variable d'environnement obligatoire est absente ou trop faible."""


class Config:
    _db_url = os.environ.get('DATABASE_URL', '')
    SQLALCHEMY_DATABASE_URI = _db_url.replace('postgresql://', 'postgresql+psycopg://', 1) if _db_url else None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    JWT_ACCESS_HOURS = int(os.environ.get('JWT_ACCESS_HOURS', 1))
    JWT_REFRESH_DAYS = int(os.environ.get('JWT_REFRESH_DAYS', 7))


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test-secret'
    JWT_SECRET_KEY = 'test-jwt-secret'


def valider_configuration(config):
    """
    Vérifie que les secrets nécessaires sont présents et suffisamment longs.

    Appelée au démarrage de l'application, hors mode test.

    :param config: Le mapping de configuration de l'application Flask.
    :raises ConfigurationError: si une variable est absente, ou si un secret
     est plus court que :data:`LONGUEUR_MINIMALE_SECRET`.
    """
    manquantes = [nom for nom in VARIABLES_REQUISES if not config.get(nom)]
    if manquantes:
        raise ConfigurationError(
            "Variables d'environnement obligatoires absentes : "
            + ", ".join(manquantes)
            + ". Voir .env.example ; générer un secret avec "
            "python -c \"import secrets; print(secrets.token_hex(32))\"."
        )

    trop_courtes = [
        nom for nom in ('SECRET_KEY', 'JWT_SECRET_KEY')
        if len(str(config.get(nom))) < LONGUEUR_MINIMALE_SECRET
    ]
    if trop_courtes:
        raise ConfigurationError(
            "Secrets trop courts (minimum "
            f"{LONGUEUR_MINIMALE_SECRET} caractères) : " + ", ".join(trop_courtes)
        )
