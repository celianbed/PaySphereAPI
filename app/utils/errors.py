from functools import wraps
from flask import jsonify


class APIError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code:
            self.status_code = status_code

    def to_dict(self):
        return {"error": self.message}


class NotFoundError(APIError):
    def __init__(self, message="Ressource non trouvée"):
        super().__init__(message, 404)


class UnauthorizedError(APIError):
    def __init__(self, message="Accès interdit"):
        super().__init__(message, 403)


class ServerError(APIError):
    def __init__(self, message="Erreur serveur"):
        super().__init__(message, 500)


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIError as e:
            return jsonify(e.to_dict()), e.status_code
        except ValueError:
            return jsonify({"erreur": "Valeur invalide fournie"}), 400
        except KeyError as e:
            return jsonify({"erreur": f"Donnée manquante : {str(e)}"}), 400
        except AttributeError as e:
            print(f"AttributeError in {func.__name__}: {e}")
            return jsonify({"erreur": "Ressource non trouvée"}), 404
        except Exception as e:
            print(f"Exception in {func.__name__}: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"erreur": "Erreur interne du serveur"}), 500
    return wrapper
