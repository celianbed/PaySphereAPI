# PaySphere API - Routes

Base URL: `/PaySphereAPI`

## Auth

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/register` | - | Créer un compte utilisateur |
| POST | `/login` | - | Se connecter (retourne access + refresh token) |
| POST | `/refresh` | Refresh | Renouveler l'access token |
| POST | `/logout` | JWT | Déconnecter (invalide l'access token) |
| POST | `/logout_refresh` | JWT | Révoquer le refresh token |

## Users

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/users/<id>` | JWT | Détails d'un utilisateur (owner only) |
| PATCH | `/users/<id>` | JWT | Modifier un utilisateur (owner only) |
| DELETE | `/users/<id>` | JWT | Supprimer un utilisateur (owner only) |
| PATCH | `/users/<id>/change-password` | JWT | Changer le mot de passe |

## Clients

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/clients` | JWT | Créer un client |
| GET | `/clients/<id>` | JWT | Détails d'un client (owner only) |
| GET | `/clients/numero/<num>` | JWT | Chercher un client par numéro |
| PATCH | `/clients/<id>` | JWT | Modifier un client (owner only) |
| DELETE | `/clients/<id>` | JWT | Supprimer un client (owner only) |

## Comptes

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/comptes` | JWT | Comptes du client connecté |
| POST | `/comptes` | JWT | Ouvrir un compte pour le client connecté |
| GET | `/comptes/<id>` | JWT | Détails d'un compte (owner only) |

## Virements

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/virement` | JWT | Effectuer un virement |
| GET | `/virement?page=1&per_page=20` | JWT | Virements du client connecté (paginé) |
| POST | `/virements/verifie-beneficiaire` | JWT | Vérifier un IBAN bénéficiaire |

## Cartes

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/cartes/<id>/opposee` | JWT | Opposer une carte (owner only) |
| GET | `/cartes/<id>/plafond` | JWT | Usage du plafond (owner only) |
| PATCH | `/cartes/<id>/plafond` | JWT | Modifier le plafond (owner only) |
| PATCH | `/cartes/<id>/paiement-en-ligne` | JWT | Toggle paiement en ligne |
| PATCH | `/cartes/<id>/paiement-sans-contact` | JWT | Toggle sans contact |

## Bénéficiaires

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/clients/beneficiaires` | JWT | Ajouter un bénéficiaire |
| DELETE | `/clients/beneficiaires/<id>` | JWT | Supprimer un bénéficiaire |

## Notifications

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/notifications` | JWT | Notifications du client connecté |
| POST | `/notifications/<id>/lu` | JWT | Marquer comme lue |

## Monitoring

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/health` | - | Status de l'API et de la BDD |

## Règles d'accès

Toute route marquée « owner only » ne retourne la ressource que si elle
appartient au porteur du jeton. Les vérifications sont centralisées dans
`app/utils/authz.py` et couvertes par `tests/test_authorization.py`.

Une ressource inexistante et une ressource appartenant à un autre client
renvoient la **même** réponse `404`. Distinguer les deux cas permettrait
d'énumérer les identifiants valides.

Les routes `GET /users` (liste de tous les utilisateurs) et `POST /users`
(création arbitraire) ont été retirées : sans modèle de rôles, elles
exposaient les données de tous les clients à n'importe quel porteur de jeton.
La création de compte passe exclusivement par `POST /register`.

## Headers requis

```
Content-Type: application/json
X-API-Key: <votre_cle_api>
Authorization: Bearer <access_token>  (pour les routes JWT)
```
