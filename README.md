# PaySphere API

API REST de l'application bancaire PaySphere. Flask, PostgreSQL, authentification
par jeton JWT.

Application cliente : [PaySphereApp](https://github.com/celianbed/PaySphereApp) (Flutter).

## Démarrage rapide avec Docker

L'environnement conteneurisé reproduit la production : même version de Python,
même serveur WSGI, même procédure de migration.

```bash
docker compose up --build
```

L'API répond alors sur <http://localhost:5000/PaySphereAPI/>, la documentation
interactive sur <http://localhost:5000/swagger>.

```bash
docker compose run --rm api python seed.py   # jeu d'essai
docker compose run --rm api pytest           # campagne de tests
docker compose down --volumes                # arrêt et remise à zéro
```

## Démarrage sans Docker

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env        # puis renseigner les variables
flask db upgrade
python wsgi.py
```

## Variables d'environnement

`DATABASE_URL`, `SECRET_KEY` et `JWT_SECRET_KEY` sont obligatoires :
l'application refuse de démarrer si l'une manque ou si un secret fait moins de
32 caractères. Ce choix est délibéré — une clé générée au démarrage produit des
déconnexions aléatoires impossibles à diagnostiquer, puisque chaque worker
signe alors avec une clé différente.

Toutes les variables sont décrites dans [.env.example](.env.example) et
déclarées dans [render.yaml](render.yaml).

## Tests

```bash
pytest                                          # campagne complète
pytest tests/test_authorization.py -v           # tests de sécurité seuls
pytest --cov=app --cov-report=term-missing      # couverture
```

`tests/test_authorization.py` vérifie le cloisonnement des données entre
clients : pour chaque ressource, qu'un client authentifié ne peut atteindre ni
lire celles d'un autre.

## Sécurité

```bash
bandit -r app config.py wsgi.py -ll    # analyse statique du code
pip-audit -r requirements.txt          # vulnérabilités des dépendances
```

Les deux commandes sont exécutées à chaque push par l'intégration continue et
bloquent le déploiement en cas d'échec.

Principes appliqués :

- **Cloisonnement.** Toute ressource appartenant à un client est résolue via
  `app/utils/authz.py`, qui vérifie le propriétaire. Aucune route ne compare un
  identifiant fourni par le client à l'identité du porteur du jeton.
- **Non-divulgation.** Une ressource inexistante et une ressource appartenant à
  un tiers renvoient la même réponse `404`, pour ne pas permettre d'énumérer
  les identifiants valides.
- **Moindre exposition.** Le cryptogramme des cartes n'est jamais restitué. Les
  routes d'administration sans modèle de rôles ont été retirées.
- **Limitation de débit.** `Flask-Limiter`, avec `ProxyFix` pour que le quota
  s'applique par client et non globalement derrière le proxy.

## Déploiement

Hébergement : [Render](https://render.com), décrit dans
[render.yaml](render.yaml).

Le déploiement automatique de Render est désactivé. La mise en production est
déclenchée par le workflow [`ci.yml`](.github/workflows/ci.yml), uniquement sur
`main` et uniquement après réussite des tests, de l'analyse de sécurité et de la
construction de l'image Docker. Le workflow attend ensuite que la nouvelle
instance réponde avant de considérer le déploiement comme réussi.

### Mise en veille de l'instance

L'offre gratuite arrête l'instance après quinze minutes sans trafic ; le réveil
demande environ une minute. L'application mobile gère cette latence
explicitement, mais pour une démonstration, mieux vaut maintenir l'instance
éveillée en interrogeant `/PaySphereAPI/health` toutes les dix minutes depuis un
service de supervision externe (cron-job.org, UptimeRobot). Cette sonde est
volontairement exemptée de clé API.

## Structure

```
app/
  models/       entités SQLAlchemy
  controllers/  logique métier et accès aux données
  routes/       points d'entrée HTTP
  utils/
    authz.py    vérifications de propriété, partagées par les routes
    errors.py   conversion des exceptions en réponses HTTP
migrations/     versions Alembic
tests/          campagne fonctionnelle et campagne de sécurité
```

La documentation des routes est disponible dans [API_ROUTES.md](API_ROUTES.md)
et sous forme interactive sur `/swagger`.
