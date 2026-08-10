"""
Point d'entrée WSGI de l'application.

En production, ce module est chargé par Gunicorn (`gunicorn wsgi:app`) et le
bloc ci-dessous n'est jamais exécuté. Il ne sert qu'au lancement manuel en
développement.
"""

import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Le débogueur Werkzeug expose une console d'exécution de code : il ne doit
    # s'activer que sur demande explicite, jamais par défaut. L'écoute est
    # limitée à la boucle locale ; pour exposer le service sur le réseau, on
    # passe par Docker et Gunicorn, qui reproduisent la production.
    app.run(
        debug=os.environ.get("FLASK_DEBUG") == "1",
        host=os.environ.get("FLASK_RUN_HOST", "127.0.0.1"),
        port=int(os.environ.get("FLASK_RUN_PORT", 5000)),
    )
