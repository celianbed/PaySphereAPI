from functools import wraps
from flask import jsonify


class APIError(Exception):
    """Classe de base pour les erreurs API personnalisées"""
    status_code = 400  # Par défaut, une erreur 400 (Bad Request)

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code:
            self.status_code = status_code

    def to_dict(self):
        return {"error": self.message}

# Erreur spécifique (ex: Ressource non trouvée)
class NotFoundError(APIError):
    def __init__(self, message="Ressource non trouvée"):
        super().__init__(message, 404)

# Erreur spécifique (ex: Accès non autorisé)
class UnauthorizedError(APIError):
    def __init__(self, message="Accès interdit"):
        super().__init__(message, 403)

class ServerError(APIError):
    def __init__(self, message="Erreur serveur"):
        super().__init__(message, 500)

def handle_exceptions(func):
    """Décorateur pour gérer les erreurs dans les routes Flask"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return jsonify({"erreur": "ID utilisateur invalide"}), 400
        except Exception as e:
            return jsonify({"erreur": "Erreur interne du serveur", "message": str(e)}), 500
    return wrapper