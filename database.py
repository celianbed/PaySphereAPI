from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config  # Importe la config que tu as déjà définie

# Créer l'engine avec la connexion PostgreSQL
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# Gérer les sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Déclarer le Base pour SQLAlchemy
Base = declarative_base()
