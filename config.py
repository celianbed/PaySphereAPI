import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:adminpass@localhost:5432/ma_base'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')
