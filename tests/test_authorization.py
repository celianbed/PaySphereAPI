"""
Tests de sécurité : cloisonnement des données entre clients.

Chaque test répond à une question unique : « un client authentifié peut-il
atteindre les données d'un autre client ? ». Ils sont volontairement séparés des
tests fonctionnels car ils constituent la campagne de tests de sécurité de
l'API et doivent pouvoir être rejoués et présentés isolément.
"""

from datetime import date

from app.models.Compte import Compte
from app.models.Notification import Notification
from app.models.Pret import Pret
from app.models.TypeVirement import TypeVirement
from app.models.Virement import Virement


class TestVirementAutorisation:
    """Contrôle du propriétaire du compte émetteur d'un virement."""

    def test_virement_depuis_le_compte_d_un_tiers_est_refuse(self, client, scenario_ids_alignes):
        """
        Un client ne peut pas émettre un virement depuis le compte d'un autre.

        Le scénario place l'identifiant du compte de la victime à la même
        valeur que l'identifiant de l'utilisateur attaquant : c'est le cas
        précis que l'ancien contrôle laissait passer.
        """
        victime = scenario_ids_alignes['victime']
        attaquant = scenario_ids_alignes['attaquant']

        reponse = client.post('/PaySphereAPI/virement', json={
            'from_account': victime['compte'].id,
            'to_account_iban': attaquant['rib'].iban,
            'montant': 1500.00,
            'type_virement': 1,
        }, headers=scenario_ids_alignes['headers_attaquant'])

        assert reponse.status_code == 404

    def test_virement_refuse_ne_deplace_aucun_fonds(self, client, db, scenario_ids_alignes):
        """Le refus doit être total : aucun solde ne bouge, aucun virement n'est écrit."""
        victime = scenario_ids_alignes['victime']
        attaquant = scenario_ids_alignes['attaquant']

        solde_victime = float(victime['compte'].get_solde())
        solde_attaquant = float(attaquant['compte'].get_solde())

        client.post('/PaySphereAPI/virement', json={
            'from_account': victime['compte'].id,
            'to_account_iban': attaquant['rib'].iban,
            'montant': 1500.00,
            'type_virement': 1,
        }, headers=scenario_ids_alignes['headers_attaquant'])

        db.session.refresh(victime['compte'])
        db.session.refresh(attaquant['compte'])

        assert float(victime['compte'].get_solde()) == solde_victime
        assert float(attaquant['compte'].get_solde()) == solde_attaquant
        assert Virement.query.count() == 0

    def test_virement_depuis_son_propre_compte_est_autorise(self, client, db, seed_refs, user1, auth_headers):
        """
        Un virement légitime reste possible même si l'identifiant du compte
        diffère de celui de l'utilisateur.

        L'ancien contrôle refusait ce cas : il bloquait les virements des
        clients dont le compte n'avait pas le même identifiant qu'eux.
        """
        # Second compte du client, dont l'identifiant ne coïncide avec aucun
        # identifiant d'utilisateur.
        autre_compte = Compte(
            client=user1['client'],
            type_compte=seed_refs['types_compte'][0],
            statut=seed_refs['statuts'][2],
            solde=1000.00,
        )
        db.session.add(autre_compte)
        db.session.commit()

        assert autre_compte.id != user1['user'].id

        reponse = client.post('/PaySphereAPI/virement', json={
            'from_account': autre_compte.id,
            'to_account_iban': user1['rib'].iban,
            'montant': 100.00,
            'type_virement': 1,
        }, headers=auth_headers)

        assert reponse.status_code == 201
        assert reponse.get_json()['success'] is True

    def test_virement_vers_soi_meme_est_refuse(self, client, user1, auth_headers):
        """Un virement d'un compte vers lui-même n'a pas de sens métier."""
        reponse = client.post('/PaySphereAPI/virement', json={
            'from_account': user1['compte'].id,
            'to_account_iban': user1['rib'].iban,
            'montant': 50.00,
            'type_virement': 1,
        }, headers=auth_headers)

        assert reponse.status_code == 400
        assert reponse.get_json()['success'] is False

    def test_virement_sans_jeton_est_refuse(self, client, user1, user2):
        reponse = client.post('/PaySphereAPI/virement', json={
            'from_account': user1['compte'].id,
            'to_account_iban': user2['rib'].iban,
            'montant': 100.00,
        })
        assert reponse.status_code == 401


class TestComptesCloisonnement:
    """La liste et le détail des comptes ne doivent exposer que le client appelant."""

    def test_liste_des_comptes_limitee_au_client_connecte(self, client, user1, user2, auth_headers):
        reponse = client.get('/PaySphereAPI/comptes', headers=auth_headers)

        assert reponse.status_code == 200
        comptes = reponse.get_json()
        assert [c['id'] for c in comptes] == [user1['compte'].id]

    def test_liste_des_comptes_ne_contient_aucun_iban_etranger(self, client, user1, user2, auth_headers):
        """Vérification explicite : l'IBAN d'un tiers ne doit apparaître nulle part."""
        reponse = client.get('/PaySphereAPI/comptes', headers=auth_headers)

        assert user2['rib'].iban not in reponse.get_data(as_text=True)

    def test_detail_du_compte_d_un_tiers_est_refuse(self, client, user1, user2, auth_headers):
        reponse = client.get(f"/PaySphereAPI/comptes/{user2['compte'].id}", headers=auth_headers)
        assert reponse.status_code == 404

    def test_compte_inexistant_et_compte_d_autrui_sont_indiscernables(self, client, user1, user2, auth_headers):
        """
        Anti-énumération : répondre 403 pour un compte existant et 404 pour un
        compte inexistant permettrait de découvrir les identifiants valides.
        """
        compte_d_autrui = client.get(f"/PaySphereAPI/comptes/{user2['compte'].id}", headers=auth_headers)
        compte_inexistant = client.get('/PaySphereAPI/comptes/999999', headers=auth_headers)

        assert compte_d_autrui.status_code == compte_inexistant.status_code
        assert compte_d_autrui.get_json() == compte_inexistant.get_json()

    def test_creation_de_compte_rattachee_au_client_connecte(self, client, user1, user2, auth_headers):
        """``POST /comptes`` ouvre un compte pour l'appelant, jamais pour un tiers."""
        reponse = client.post('/PaySphereAPI/comptes', json={
            'client_id': user2['client'].id,
        }, headers=auth_headers)

        assert reponse.status_code == 201
        nouveau = Compte.query.get(reponse.get_json()['id'])
        assert nouveau.client_id == user1['client'].id

    def test_liste_des_comptes_sans_jeton_est_refusee(self, client, user1):
        assert client.get('/PaySphereAPI/comptes').status_code == 401


class TestVirementsCloisonnement:
    """L'historique des virements ne doit contenir que ceux du client appelant."""

    def test_historique_limite_aux_comptes_du_client(self, client, db, user1, user2, auth_headers, seed_refs):
        # Un virement entre deux tiers, auquel le client appelant est étranger.
        tiers_a = user2['compte']
        virement_etranger = Virement(
            compte_source=tiers_a,
            compte_destination=tiers_a,
            montant=42.00,
            date_virement=date.today(),
            statut=seed_refs['statuts'][1],
            type_virement=TypeVirement.query.get(1),
        )
        db.session.add(virement_etranger)
        db.session.commit()

        reponse = client.get('/PaySphereAPI/virement', headers=auth_headers)

        assert reponse.status_code == 200
        assert reponse.get_json()['total'] == 0

    def test_historique_contient_les_virements_du_client(self, client, user1, user2, auth_headers):
        client.post('/PaySphereAPI/virement', json={
            'from_account': user1['compte'].id,
            'to_account_iban': user2['rib'].iban,
            'montant': 30.00,
            'type_virement': 1,
        }, headers=auth_headers)

        reponse = client.get('/PaySphereAPI/virement', headers=auth_headers)
        assert reponse.get_json()['total'] == 1

    def test_le_beneficiaire_voit_le_virement_recu(self, client, user1, user2, auth_headers, auth_headers_user2):
        client.post('/PaySphereAPI/virement', json={
            'from_account': user1['compte'].id,
            'to_account_iban': user2['rib'].iban,
            'montant': 30.00,
            'type_virement': 1,
        }, headers=auth_headers)

        reponse = client.get('/PaySphereAPI/virement', headers=auth_headers_user2)
        assert reponse.get_json()['total'] == 1


class TestRoutesSupprimees:
    """Les routes d'administration sans modèle de rôles ont été retirées."""

    def test_liste_globale_des_utilisateurs_indisponible(self, client, user1, user2, auth_headers):
        reponse = client.get('/PaySphereAPI/users', headers=auth_headers)
        assert reponse.status_code in (404, 405)

    def test_creation_arbitraire_d_utilisateur_indisponible(self, client, user1, auth_headers):
        reponse = client.post('/PaySphereAPI/users', json={
            'id': 999, 'nom': 'X', 'prenom': 'Y', 'email': 'x@y.z',
            'username': 'xy', 'active': True, 'password': 'MotDePasse1!@',
        }, headers=auth_headers)
        assert reponse.status_code in (404, 405)


class TestClientCloisonnement:
    def test_fiche_client_d_un_tiers_par_id_est_refusee(self, client, user1, user2, auth_headers):
        reponse = client.get(f"/PaySphereAPI/clients/{user2['client'].id}", headers=auth_headers)
        assert reponse.status_code in (403, 404)

    def test_fiche_client_d_un_tiers_par_numero_est_refusee(self, client, user1, user2, auth_headers):
        reponse = client.get(f"/PaySphereAPI/clients/numero/{user2['client'].num_client}",
                             headers=auth_headers)
        assert reponse.status_code in (403, 404)

    def test_modification_du_client_d_un_tiers_est_refusee(self, client, user1, user2, auth_headers):
        reponse = client.patch(f"/PaySphereAPI/clients/{user2['client'].id}",
                               json={'nom': 'Pirate'}, headers=auth_headers)
        assert reponse.status_code in (403, 404)
        assert user2['client'].nom != 'Pirate'


class TestUserCloisonnement:
    def test_profil_d_un_tiers_est_refuse(self, client, user1, user2, auth_headers):
        reponse = client.get(f"/PaySphereAPI/users/{user2['user'].id}", headers=auth_headers)
        assert reponse.status_code == 403

    def test_suppression_d_un_tiers_est_refusee(self, client, user1, user2, auth_headers):
        reponse = client.delete(f"/PaySphereAPI/users/{user2['user'].id}", headers=auth_headers)
        assert reponse.status_code == 403

    def test_changement_de_mot_de_passe_d_un_tiers_est_refuse(self, client, user1, user2, auth_headers):
        reponse = client.patch(f"/PaySphereAPI/users/{user2['user'].id}/change-password", json={
            'ancien_password': 'TestPass123!@',
            'nouveau_password': 'NouveauPass1!@',
        }, headers=auth_headers)
        assert reponse.status_code == 403


class TestNotificationCloisonnement:
    def test_notification_d_un_tiers_non_marquable(self, client, db, user1, user2, auth_headers):
        notif = Notification(
            client_id=user2['client'].id,
            type_notification='test',
            message='Notification privée',
        )
        db.session.add(notif)
        db.session.commit()

        reponse = client.post(f'/PaySphereAPI/notifications/{notif.id}/lu', headers=auth_headers)
        assert reponse.status_code == 403

    def test_liste_des_notifications_limitee_au_client(self, client, db, user1, user2, auth_headers):
        db.session.add(Notification(
            client_id=user2['client'].id,
            type_notification='test',
            message='Notification privée',
        ))
        db.session.commit()

        reponse = client.get('/PaySphereAPI/notifications', headers=auth_headers)
        assert reponse.status_code == 200
        assert reponse.get_json() == []


class TestPretCloisonnement:
    def test_pret_d_un_tiers_inaccessible(self, client, db, user1, user2, auth_headers):
        pret = Pret(client_id=user2['client'].id, montant_pret=1000,
                    taux_interet=3.5, date_demande=date.today(),
                    date_echeance=date(date.today().year + 1, date.today().month, 1),
                    statut="en_attente")
        db.session.add(pret)
        db.session.commit()

        reponse = client.get(f'/PaySphereAPI/prets/{pret.id}', headers=auth_headers)
        assert reponse.status_code == 403

    def test_annulation_du_pret_d_un_tiers_refusee(self, client, db, user1, user2, auth_headers):
        pret = Pret(client_id=user2['client'].id, montant_pret=1000,
                    taux_interet=3.5, date_demande=date.today(),
                    date_echeance=date(date.today().year + 1, date.today().month, 1),
                    statut="en_attente")
        db.session.add(pret)
        db.session.commit()

        reponse = client.post(f'/PaySphereAPI/prets/{pret.id}/annuler', headers=auth_headers)
        assert reponse.status_code == 403


class TestRobustesseEntrees:
    """Une entrée malformée doit produire un 4xx explicite, jamais un 500."""

    def test_montant_non_numerique(self, client, user1, user2, auth_headers):
        reponse = client.post('/PaySphereAPI/virement', json={
            'from_account': user1['compte'].id,
            'to_account_iban': user2['rib'].iban,
            'montant': 'abc',
        }, headers=auth_headers)
        assert reponse.status_code == 400

    def test_compte_emetteur_absent(self, client, user1, user2, auth_headers):
        reponse = client.post('/PaySphereAPI/virement', json={
            'to_account_iban': user2['rib'].iban,
            'montant': 100,
        }, headers=auth_headers)
        assert reponse.status_code == 400

    def test_corps_vide(self, client, user1, auth_headers):
        reponse = client.post('/PaySphereAPI/virement', json={}, headers=auth_headers)
        assert reponse.status_code == 400

    def test_montant_infini(self, client, user1, user2, auth_headers):
        reponse = client.post('/PaySphereAPI/virement', json={
            'from_account': user1['compte'].id,
            'to_account_iban': user2['rib'].iban,
            'montant': float('inf'),
        }, headers=auth_headers)
        assert reponse.status_code == 400

    def test_montant_negatif(self, client, user1, user2, auth_headers):
        reponse = client.post('/PaySphereAPI/virement', json={
            'from_account': user1['compte'].id,
            'to_account_iban': user2['rib'].iban,
            'montant': -100,
        }, headers=auth_headers)
        assert reponse.status_code == 400


class TestDonneesSensibles:
    """Certaines données ne doivent jamais quitter le serveur."""

    def test_le_code_de_securite_de_carte_n_est_jamais_expose(self, client, user1, auth_headers):
        """
        Le cryptogramme visuel ne doit apparaître dans aucune réponse : le
        conserver et le restituer est proscrit par la norme PCI-DSS.
        """
        reponse = client.get('/PaySphereAPI/comptes', headers=auth_headers)
        assert 'code_securite' not in reponse.get_data(as_text=True)

    def test_le_hash_du_mot_de_passe_n_est_jamais_expose(self, client, user1, auth_headers):
        reponse = client.get(f"/PaySphereAPI/users/{user1['user'].id}", headers=auth_headers)
        corps = reponse.get_data(as_text=True)
        assert 'password_hash' not in corps
        assert '$2b$' not in corps
