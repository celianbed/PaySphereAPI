import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    _db_url = os.environ.get('DATABASE_URL', '')
    SQLALCHEMY_DATABASE_URI = _db_url.replace('postgresql://', 'postgresql+psycopg://', 1) if _db_url else None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32).hex())
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', os.urandom(32).hex())

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    JWT_ACCESS_HOURS = int(os.environ.get('JWT_ACCESS_HOURS', 1))
    JWT_REFRESH_DAYS = int(os.environ.get('JWT_REFRESH_DAYS', 7))


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
