from app.controllers.virement_controller import VirementController
from app.models.Notification import Notification


class TestVirementController:
    def test_create_virement_success(self, db, user1, user2):
        solde_before_src = float(user1['compte'].solde)
        solde_before_dst = float(user2['compte'].solde)

        ok, msg, virement = VirementController.create_virement({
            'from_account': user1['compte'].id,
            'to_account_iban': user2['rib'].iban,
            'montant': 500.00,
            'type_virement': 1,
        })

        assert ok is True
        assert virement is not None
        assert float(user1['compte'].solde) == solde_before_src - 500.00
        assert float(user2['compte'].solde) == solde_before_dst + 500.00

    def test_create_virement_insufficient_balance(self, db, user1, user2):
        result = VirementController.create_virement({
            'from_account': user1['compte'].id,
            'to_account_iban': user2['rib'].iban,
            'montant': 999999.00,
            'type_virement': 1,
        })
        ok, msg = result[0], result[1]

        assert ok is False
        assert "Solde insuffisant" in msg

    def test_create_virement_negative_amount(self, db, user1, user2):
        result = VirementController.create_virement({
            'from_account': user1['compte'].id,
            'to_account_iban': user2['rib'].iban,
            'montant': -100.00,
            'type_virement': 1,
        })
        ok, msg = result[0], result[1]

        assert ok is False

    def test_create_virement_unknown_source(self, db, user1, user2):
        result = VirementController.create_virement({
            'from_account': 9999,
            'to_account_iban': user2['rib'].iban,
            'montant': 100.00,
            'type_virement': 1,
        })
        ok, msg = result[0], result[1]

        assert ok is False
        assert "non trouvé" in msg

    def test_create_virement_unknown_destination(self, db, user1):
        result = VirementController.create_virement({
            'from_account': user1['compte'].id,
            'to_account_iban': 'FR00INVALIDIBAN',
            'montant': 100.00,
            'type_virement': 1,
        })
        ok, msg = result[0], result[1]

        assert ok is False
        assert "non trouvé" in msg.lower() or "non trouvée" in msg.lower()

    def test_virement_creates_notification(self, db, user1, user2):
        VirementController.create_virement({
            'from_account': user1['compte'].id,
            'to_account_iban': user2['rib'].iban,
            'montant': 100.00,
            'type_virement': 1,
        })

        notif = Notification.query.filter_by(client_id=user2['client'].id).first()
        assert notif is not None
        assert "reçu" in notif.message
        assert "100.00" in notif.message


class TestVirementEndpoint:
    def test_create_virement_endpoint(self, client, user1, user2, auth_headers):
        resp = client.post('/PaySphereAPI/virement', json={
            'from_account': user1['compte'].id,
            'to_account_iban': user2['rib'].iban,
            'montant': 200.00,
            'type_virement': 1,
        }, headers=auth_headers)
        assert resp.status_code == 201
        data = resp.get_json()
        assert data['success'] is True

    def test_create_virement_unauthorized(self, client, user1, user2, auth_headers_user2):
        # 404 et non 403 : distinguer « compte inexistant » de « compte d'un
        # tiers » permettrait d'énumérer les identifiants de comptes valides.
        # Le cloisonnement complet est vérifié dans tests/test_authorization.py.
        resp = client.post('/PaySphereAPI/virement', json={
            'from_account': user1['compte'].id,
            'to_account_iban': user2['rib'].iban,
            'montant': 200.00,
            'type_virement': 1,
        }, headers=auth_headers_user2)
        assert resp.status_code == 404

    def test_verify_beneficiaire_exists(self, client, user2, auth_headers):
        resp = client.post('/PaySphereAPI/virements/verifie-beneficiaire', json={
            'to_account_iban': user2['rib'].iban,
        }, headers=auth_headers)
        assert resp.status_code == 200
        assert resp.get_json()['valid'] is True

    def test_verify_beneficiaire_not_found(self, client, user1, auth_headers):
        resp = client.post('/PaySphereAPI/virements/verifie-beneficiaire', json={
            'to_account_iban': 'FR00DOESNOTEXIST',
        }, headers=auth_headers)
        assert resp.status_code == 404
        assert resp.get_json()['valid'] is False
