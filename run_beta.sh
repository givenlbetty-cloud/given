#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════
# 🚀 SCRIPT DÉMARRAGE SERVEUR BETA
# Lance le serveur Django en environnement BETA isolé
# ═══════════════════════════════════════════════════════════════════════

set -e

# Charger les variables d'environnement
if [ ! -f ".env.beta" ]; then
    echo "❌ Fichier .env.beta non trouvé!"
    echo "Créez-le: cp .env.beta.example .env.beta"
    exit 1
fi

export $(cat .env.beta | xargs)

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🚀 SERVEUR BETA - ENVIRONNEMENT DE TEST ISOLÉ            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Afficher la configuration
echo "📌 Configuration Beta:"
echo "  🌐 ALLOWED_HOSTS: $ALLOWED_HOSTS"
echo "  📊 Database: $DATABASE_NAME"
echo "  📁 Médias: $MEDIA_ROOT"
echo "  🔐 Basic Auth: $ENABLE_BASIC_AUTH"
echo "  🐛 DEBUG: $DEBUG"
echo ""

# Créer les dossiers s'ils n'existent pas
mkdir -p media_beta
mkdir -p logs

# Lancer le serveur
echo "🚀 Démarrage du serveur..."
echo ""

python3 manage.py runserver \
    --settings=atj_site.settings_beta \
    0.0.0.0:8000
