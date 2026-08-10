# syntax=docker/dockerfile:1

# Version alignée sur PYTHON_VERSION de render.yaml, afin que l'image locale
# exécute le même interpréteur que la production.
ARG PYTHON_VERSION=3.11.9

# ---------------------------------------------------------------------------
# Étape 1 — construction des dépendances
#
# Les dépendances sont installées dans un environnement virtuel isolé, copié
# tel quel dans l'image finale. Les outils de compilation restent dans cette
# étape et n'alourdissent ni n'exposent l'image livrée.
# ---------------------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---------------------------------------------------------------------------
# Étape 2 — image d'exécution
# ---------------------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS runtime

# PYTHONDONTWRITEBYTECODE : pas de .pyc dans un système de fichiers en lecture seule.
# PYTHONUNBUFFERED : les journaux sortent immédiatement, sans tampon.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    FLASK_APP=wsgi.py

# curl sert uniquement à la sonde de santé du conteneur.
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && rm -rf /var/lib/apt/lists/*

# L'application ne s'exécute pas en root : une éventuelle exécution de code
# arbitraire reste confinée à un compte sans privilèges.
RUN useradd --create-home --shell /usr/sbin/nologin paysphere

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
COPY --chown=paysphere:paysphere . .

USER paysphere

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -fsS http://localhost:5000/PaySphereAPI/health || exit 1

# Deux workers : suffisant pour la démonstration, et surtout cohérent avec le
# fait que les jetons doivent rester valides d'un worker à l'autre — ce qui
# n'était pas le cas tant que les secrets étaient générés au démarrage.
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-"]
