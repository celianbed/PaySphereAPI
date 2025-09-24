import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://neondb_owner:npg_t1Hcgsq4XFSw@ep-lucky-fog-adr97bc8-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require' //postgresql://admin:adminpass@192.168.1.20:5432/PaySphereDB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
