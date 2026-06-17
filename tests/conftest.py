import os
import pytest
from datetime import date
from flask_jwt_extended import create_access_token

from app import create_app, db as _db
from app.models.User import User
from app.models.Client import Client
from app.models.Compte import Compte
from app.models.Statut import Statut
from app.models.TypeCompte import TypeCompte
from app.models.TypeCarte import TypeCarte
from app.models.TypeVirement import TypeVirement
from app.models.TypeTransaction import TypeTransaction
from app.models.Authentification import Authentification
from app.models.Rib import Rib


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test-secret'
    JWT_SECRET_KEY = 'test-jwt-secret'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    RATELIMIT_ENABLED = False


@pytest.fixture(scope='session')
def app():
    os.environ.pop('API_KEY', None)
    app = create_app(config_class=TestConfig)
    yield app


@pytest.fixture(autouse=True)
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def seed_refs(db):
    statuts = [
        Statut(id=1, nom="Inactif"),
        Statut(id=2, nom="Terminé"),
        Statut(id=3, nom="Actif"),
        Statut(id=4, nom="En attente"),
        Statut(id=5, nom="Bloqué"),
    ]
    types_compte = [
        TypeCompte(id=1, nom="Courant"),
        TypeCompte(id=2, nom="Épargne"),
    ]
    types_carte = [TypeCarte(id=1, nom="Visa Classic")]
    types_virement = [
        TypeVirement(id=1, nom="Instantané"),
        TypeVirement(id=2, nom="Standard"),
    ]
    types_transaction = [
        TypeTransaction(id=1, nom="Débit"),
        TypeTransaction(id=2, nom="Crédit"),
        TypeTransaction(id=3, nom="Virement"),
    ]
    for items in [statuts, types_compte, types_carte, types_virement, types_transaction]:
        db.session.add_all(items)
    db.session.commit()
    return {'statuts': statuts, 'types_compte': types_compte}


def _make_user(db, seed_refs, uid, nom, prenom, email, username, num_client, solde=2000.00):
    user = User(id=uid, nom=nom, prenom=prenom, email=email, username=username)
    db.session.add(user)
    db.session.flush()

    auth = Authentification(user=user, password="TestPass123!@")
    db.session.add(auth)
    db.session.flush()

    cli = Client(
        id=uid, user=user, num_client=num_client,
        nom=nom, prenom=prenom, email=email,
        adresse="12 Rue Test, 75001 Paris",
        numero_de_telephone="0612345678",
        date_naissance=date(1990, 5, 15),
    )
    db.session.add(cli)
    db.session.flush()

    compte = Compte(
        client=cli,
        type_compte=seed_refs['types_compte'][0],
        statut=seed_refs['statuts'][2],
        solde=solde,
    )
    db.session.add(compte)
    db.session.flush()

    iban, _ = Rib.generate_iban()
    rib = Rib(
        compte=compte, iban=iban, bic="PAYSFRPP",
        titulaire_compte=f"{prenom} {nom}",
        banque="PaySphere", agence="Test", adresse_banque="1 Rue Test",
    )
    db.session.add(rib)
    db.session.commit()

    return {'user': user, 'client': cli, 'compte': compte, 'rib': rib, 'auth': auth}


@pytest.fixture
def user1(db, seed_refs):
    return _make_user(db, seed_refs, 1, "Dupont", "Jean", "jean@test.com", "jdupont", 10001)


@pytest.fixture
def user2(db, seed_refs):
    return _make_user(db, seed_refs, 2, "Martin", "Sophie", "sophie@test.com", "smartin", 10002)


@pytest.fixture
def auth_headers(app, user1):
    with app.app_context():
        token = create_access_token(identity=str(user1['user'].id))
    return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}


@pytest.fixture
def auth_headers_user2(app, user2):
    with app.app_context():
        token = create_access_token(identity=str(user2['user'].id))
    return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
