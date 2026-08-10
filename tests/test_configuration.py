"""Tests du durcissement de la configuration et des en-têtes de sécurité."""

import pytest

from config import (
    LONGUEUR_MINIMALE_SECRET,
    ConfigurationError,
    valider_configuration,
)

SECRET_VALIDE = 'a' * LONGUEUR_MINIMALE_SECRET


def _configuration_complete(**surcharges):
    base = {
        'DATABASE_URL': 'postgresql+psycopg://user:pass@localhost/db',
        'SECRET_KEY': SECRET_VALIDE,
        'JWT_SECRET_KEY': 'b' * LONGUEUR_MINIMALE_SECRET,
    }
    base.update(surcharges)
    return base


class TestValidationConfiguration:
    def test_configuration_complete_acceptee(self):
        valider_configuration(_configuration_complete())

    @pytest.mark.parametrize('variable', ['DATABASE_URL', 'SECRET_KEY', 'JWT_SECRET_KEY'])
    def test_variable_absente_refusee(self, variable):
        """
        Le démarrage doit échouer bruyamment plutôt que de se rabattre sur une
        clé aléatoire, qui invaliderait les jetons à chaque redémarrage et
        différerait d'un worker Gunicorn à l'autre.
        """
        configuration = _configuration_complete(**{variable: None})

        with pytest.raises(ConfigurationError) as erreur:
            valider_configuration(configuration)

        assert variable in str(erreur.value)

    def test_secret_trop_court_refuse(self):
        configuration = _configuration_complete(SECRET_KEY='court')

        with pytest.raises(ConfigurationError) as erreur:
            valider_configuration(configuration)

        assert 'SECRET_KEY' in str(erreur.value)

    def test_message_liste_toutes_les_variables_manquantes(self):
        configuration = _configuration_complete(SECRET_KEY=None, JWT_SECRET_KEY=None)

        with pytest.raises(ConfigurationError) as erreur:
            valider_configuration(configuration)

        message = str(erreur.value)
        assert 'SECRET_KEY' in message and 'JWT_SECRET_KEY' in message


class TestEnTetesSecurite:
    def test_en_tetes_presents_sur_les_reponses(self, client, user1, auth_headers):
        reponse = client.get(f"/PaySphereAPI/users/{user1['user'].id}", headers=auth_headers)

        assert reponse.headers['X-Content-Type-Options'] == 'nosniff'
        assert reponse.headers['X-Frame-Options'] == 'DENY'
        assert 'Strict-Transport-Security' in reponse.headers
        assert reponse.headers['Referrer-Policy'] == 'no-referrer'

    def test_en_tetes_presents_sur_les_erreurs(self, client):
        reponse = client.get('/PaySphereAPI/comptes')

        assert reponse.status_code == 401
        assert reponse.headers['X-Content-Type-Options'] == 'nosniff'


class TestSondeSupervision:
    def test_health_repond_sans_authentification(self, client):
        """La sonde doit rester joignable pour le keep-alive et la supervision."""
        reponse = client.get('/PaySphereAPI/health')

        assert reponse.status_code == 200
        assert reponse.get_json()['status'] == 'ok'
