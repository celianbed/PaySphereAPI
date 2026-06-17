from app.models.User import User
from app.models.Rib import Rib


class TestPasswordSchema:
    def test_valid_password(self):
        assert User.is_schema_valid("TestPass123!@") is True

    def test_too_short(self):
        assert User.is_schema_valid("Short1!") is False

    def test_too_long(self):
        assert User.is_schema_valid("A" * 21 + "a1!") is False

    def test_no_uppercase(self):
        assert User.is_schema_valid("testpass123!@") is False

    def test_no_lowercase(self):
        assert User.is_schema_valid("TESTPASS123!@") is False

    def test_no_digit(self):
        assert User.is_schema_valid("TestPassWord!@") is False

    def test_no_symbol(self):
        assert User.is_schema_valid("TestPass12345") is False

    def test_with_spaces(self):
        assert User.is_schema_valid("Test Pass123!") is False


class TestEmailValidation:
    def test_valid_email(self):
        assert User.is_email_valid("user@example.com") is True

    def test_invalid_email_no_at(self):
        assert User.is_email_valid("userexample.com") is False

    def test_invalid_email_no_domain(self):
        assert User.is_email_valid("user@") is False


class TestCompte:
    def test_can_make_transfer_success(self, user1):
        compte = user1['compte']
        ok, msg = compte.can_make_transfer(500.00)
        assert ok is True

    def test_can_make_transfer_insufficient_balance(self, user1):
        compte = user1['compte']
        ok, msg = compte.can_make_transfer(99999.00)
        assert ok is False
        assert "Solde insuffisant" in msg

    def test_can_make_transfer_negative_amount(self, user1):
        compte = user1['compte']
        ok, msg = compte.can_make_transfer(-100.00)
        assert ok is False
        assert "positif" in msg

    def test_can_make_transfer_inactive_account(self, db, seed_refs, user1):
        compte = user1['compte']
        compte.statut = seed_refs['statuts'][0]  # Inactif
        db.session.commit()
        ok, msg = compte.can_make_transfer(100.00)
        assert ok is False
        assert "actif" in msg.lower()


class TestAuthentification:
    def test_password_valid(self, user1):
        auth = user1['auth']
        assert auth.is_password_valid("TestPass123!@") is True

    def test_password_invalid(self, user1):
        auth = user1['auth']
        assert auth.is_password_valid("WrongPassword1!") is False


class TestRib:
    def test_generate_iban_format(self):
        iban, country = Rib.generate_iban()
        assert country == "FR"
        assert iban.startswith("FR")
        assert len(iban) == 19

    def test_generate_iban_custom_country(self):
        iban, country = Rib.generate_iban("DE")
        assert country == "DE"
        assert iban.startswith("DE")


class TestUserToDict:
    def test_user_to_dict_all_fields(self, user1):
        data = user1['user'].to_dict()
        assert data['nom'] == "Dupont"
        assert data['prenom'] == "Jean"
        assert data['email'] == "jean@test.com"
        assert data['username'] == "jdupont"
        assert data['active'] is True

    def test_user_to_dict_filtered(self, user1):
        data = user1['user'].to_dict(fields=['nom', 'prenom'])
        assert 'nom' in data
        assert 'prenom' in data
        assert 'email' not in data


class TestCompteToDict:
    def test_compte_to_dict(self, user1):
        data = user1['compte'].to_dict()
        assert data['solde'] == 2000.00
        assert data['type_compte_nom'] == "Courant"
        assert data['statut_nom'] == "Actif"
        assert 'rib' in data

    def test_compte_to_dict_with_exclude(self, user1):
        data = user1['compte'].to_dict(exclude=['rib', 'cartes'])
        assert 'rib' not in data
        assert 'cartes' not in data
        assert 'solde' in data
