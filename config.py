import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:adminpass@192.168.1.20:5432/PaySphereDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
