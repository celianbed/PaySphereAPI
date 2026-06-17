"""
Script de seed pour peupler la base de données avec des données de test.
Usage: python seed.py
"""
from datetime import datetime, date, timedelta
from app import create_app, db
from app.models.User import User
from app.models.Client import Client
from app.models.Compte import Compte
from app.models.Statut import Statut
from app.models.TypeCompte import TypeCompte
from app.models.TypeCarte import TypeCarte
from app.models.TypeVirement import TypeVirement
from app.models.TypeTransaction import TypeTransaction
from app.models.Carte import Carte
from app.models.Rib import Rib
from app.models.Authentification import Authentification
from app.models.Beneficiaire import Beneficiaire
from app.models.Notification import Notification
from app.routes import bcrypt


def seed():
    app = create_app()

    with app.app_context():
        print("Suppression des anciennes données...")
        db.drop_all()
        db.create_all()

        # --- Statuts ---
        statuts = [
            Statut(id=1, nom="Inactif"),
            Statut(id=2, nom="Terminé"),
            Statut(id=3, nom="Actif"),
            Statut(id=4, nom="En attente"),
            Statut(id=5, nom="Bloqué"),
        ]
        db.session.add_all(statuts)
        db.session.commit()
        print("Statuts créés.")

        # --- Types de compte ---
        types_compte = [
            TypeCompte(id=1, nom="Courant"),
            TypeCompte(id=2, nom="Épargne"),
            TypeCompte(id=3, nom="Professionnel"),
        ]
        db.session.add_all(types_compte)
        db.session.commit()
        print("Types de compte créés.")

        # --- Types de carte ---
        types_carte = [
            TypeCarte(id=1, nom="Visa Classic"),
            TypeCarte(id=2, nom="Visa Premier"),
            TypeCarte(id=3, nom="Mastercard Gold"),
        ]
        db.session.add_all(types_carte)
        db.session.commit()
        print("Types de carte créés.")

        # --- Types de virement ---
        types_virement = [
            TypeVirement(id=1, nom="Instantané"),
            TypeVirement(id=2, nom="Standard"),
            TypeVirement(id=3, nom="Programmé"),
        ]
        db.session.add_all(types_virement)
        db.session.commit()
        print("Types de virement créés.")

        # --- Types de transaction ---
        types_transaction = [
            TypeTransaction(id=1, nom="Débit"),
            TypeTransaction(id=2, nom="Crédit"),
            TypeTransaction(id=3, nom="Virement"),
        ]
        db.session.add_all(types_transaction)
        db.session.commit()
        print("Types de transaction créés.")

        # --- Utilisateurs et Clients ---
        # Mot de passe de test : TestPass123!@
        test_password = "TestPass123!@"

        users_data = [
            {"id": 1, "nom": "Dupont", "prenom": "Jean", "email": "jean.dupont@email.com", "username": "jdupont",
             "num_client": 100001, "adresse": "12 Rue de la Paix, 75002 Paris",
             "telephone": "0612345678", "date_naissance": date(1990, 5, 15)},
            {"id": 2, "nom": "Martin", "prenom": "Sophie", "email": "sophie.martin@email.com", "username": "smartin",
             "num_client": 100002, "adresse": "45 Avenue des Champs-Élysées, 75008 Paris",
             "telephone": "0623456789", "date_naissance": date(1985, 8, 22)},
            {"id": 3, "nom": "Bernard", "prenom": "Lucas", "email": "lucas.bernard@email.com", "username": "lbernard",
             "num_client": 100003, "adresse": "8 Boulevard Haussmann, 75009 Paris",
             "telephone": "0634567890", "date_naissance": date(1995, 1, 10)},
        ]

        for u_data in users_data:
            user = User(
                id=u_data["id"],
                nom=u_data["nom"],
                prenom=u_data["prenom"],
                email=u_data["email"],
                username=u_data["username"],
            )
            db.session.add(user)
            db.session.commit()

            auth = Authentification(
                user=user,
                password=test_password,
                derniere_connexion=None,
            )
            db.session.add(auth)
            db.session.commit()

            client = Client(
                id=u_data["id"],
                user=user,
                num_client=u_data["num_client"],
                nom=u_data["nom"],
                prenom=u_data["prenom"],
                email=u_data["email"],
                adresse=u_data["adresse"],
                numero_de_telephone=u_data["telephone"],
                date_naissance=u_data["date_naissance"],
            )
            db.session.add(client)
            db.session.commit()

            compte = Compte(
                client=client,
                type_compte=types_compte[0],
                statut=statuts[2],
                solde=1500.00 + (u_data["id"] * 500),
            )
            db.session.add(compte)
            db.session.commit()

            iban, country = Rib.generate_iban()
            rib = Rib(
                compte=compte,
                iban=iban,
                bic="PAYSFRPP",
                titulaire_compte=f"{u_data['prenom']} {u_data['nom']}",
                banque="PaySphere",
                agence="Paris Centre",
                adresse_banque="1 Place de la Bourse, 75002 Paris",
            )
            db.session.add(rib)
            db.session.commit()

            carte = Carte(
                numero_carte=f"4970{''.join([str((u_data['id'] * 1234 + i) % 10) for i in range(12)])}",
                date_expiration=date.today() + timedelta(days=365 * 3),
                code_securite=str(100 + u_data["id"] * 111),
                type_carte=types_carte[0],
            )
            carte.compte = compte
            db.session.add(carte)
            db.session.commit()

            print(f"  Utilisateur {u_data['username']} créé (client #{u_data['num_client']})")

        # --- Bénéficiaires ---
        client1 = Client.query.get(1)
        client2 = Client.query.get(2)
        compte2_rib = Client.query.get(2).comptes[0].rib

        benef = Beneficiaire(nom="Sophie Martin", iban=compte2_rib.iban, client=client1)
        db.session.add(benef)
        db.session.commit()
        print("Bénéficiaire ajouté.")

        # --- Notifications ---
        notif = Notification(
            client_id=1,
            type_notification="bienvenue",
            message="Bienvenue sur PaySphere ! Votre compte a été créé avec succès.",
        )
        db.session.add(notif)
        db.session.commit()
        print("Notification créée.")

        print("\n=== SEED TERMINÉ ===")
        print(f"\nIdentifiants de test (même mot de passe pour tous) :")
        print(f"  Mot de passe : {test_password}")
        print()
        for u_data in users_data:
            client = Client.query.get(u_data["id"])
            compte = client.comptes[0]
            print(f"  {u_data['prenom']} {u_data['nom']}:")
            print(f"    Username   : {u_data['username']}")
            print(f"    Num client : {u_data['num_client']}")
            print(f"    IBAN       : {compte.rib.iban}")
            print(f"    Solde      : {float(compte.solde):.2f} €")
            print()


if __name__ == "__main__":
    seed()
