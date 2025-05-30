#!/bin/bash

# Config : à adapter une seule fois
PI_USER=celian
PI_HOST=192.168.1.42
REMOTE_DIR=/home/celian/API/PaySphereAPI
LOCAL_DIR=./PaySphereAPI
VENV_ACTIVATE="$REMOTE_DIR/.venv/bin/activate"
APP_FILE=app.py

echo "🔁 Déploiement en cours vers le Raspberry Pi..."

# 1. Synchroniser les fichiers
rsync -avz --delete $LOCAL_DIR/ $PI_USER@$PI_HOST:$REMOTE_DIR/

# 2. Redémarrer l'API sur le Raspberry Pi
echo "🚀 Redémarrage de l'API Flask..."

# shellcheck disable=SC2087
ssh $PI_USER@$PI_HOST << EOF
cd $REMOTE_DIR
source $VENV_ACTIVATE
# Tuer l'ancien processus Flask si besoin
pkill -f "$APP_FILE"
# Lancer en arrière-plan et enregistrer dans un log
nohup python $APP_FILE > flask.log 2>&1 &
EOF

echo "✅ Déploiement terminé. API relancée sur le Pi."
