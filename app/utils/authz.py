"""Ownership checks shared by every customer-facing endpoint.

Rationale
---------
Authorisation used to be re-implemented inline in each route, which allowed two
classes of defect to appear:

* comparing an *account* identifier with a *user* identifier, which silently
  granted access whenever the two happened to be equal (see ``/virement``);
* listing endpoints that returned every row of a table to any authenticated
  caller.

Every resource a customer can reach must therefore be resolved through one of
the helpers below, so that the ownership rule lives in a single auditable place.

Enumeration
-----------
A missing resource and a resource owned by somebody else both raise
:class:`~app.utils.errors.NotFoundError`. Returning ``403`` for the second case
would confirm that a given identifier exists and let an attacker enumerate the
account, card or loan identifiers of other customers.
"""

from flask_jwt_extended import get_jwt_identity

from app.utils.errors import NotFoundError


def current_user_id() -> int:
    """Return the identifier of the authenticated user.

    The identity is stored as a string in the JWT (``create_access_token`` is
    called with ``str(user.id)``), so it is converted back to ``int`` here to
    avoid the string/int comparison mistakes that motivated this module.
    """
    return int(get_jwt_identity())


def current_user():
    """Return the authenticated :class:`~app.models.User.User`.

    :raises NotFoundError: if the token references a user that no longer exists.
    """
    from app.controllers.user_controller import UserController

    user = UserController.get_user_by_id(current_user_id())
    if user is None:
        raise NotFoundError("Utilisateur non trouvé")
    return user


def current_client():
    """Return the :class:`~app.models.Client.Client` owned by the caller.

    :raises NotFoundError: if the authenticated user has no customer record.
    """
    user = current_user()
    if user.client is None:
        raise NotFoundError("Client non trouvé")
    return user.client


def _belongs_to_caller(client) -> bool:
    """Return whether ``client`` is the customer record of the caller."""
    if client is None or client.user is None:
        return False
    return client.user.get_id() == current_user_id()


def owned_compte(compte_id):
    """Return account ``compte_id`` only when it belongs to the caller.

    :raises NotFoundError: if the account does not exist *or* belongs to
        somebody else — the two cases are deliberately indistinguishable.
    """
    from app.controllers.compte_controller import CompteController

    compte = CompteController.get_compte_by_id(compte_id)
    if compte is None or not _belongs_to_caller(compte.client):
        raise NotFoundError("Compte non trouvé")
    return compte


def owned_client(client_id):
    """Return customer ``client_id`` only when it is the caller's own record.

    :raises NotFoundError: if the customer does not exist *or* is not the
        caller.
    """
    from app.controllers.client_controller import ClientController

    client = ClientController.get_client_by_id(client_id)
    if client is None or not _belongs_to_caller(client):
        raise NotFoundError("Client non trouvé")
    return client
