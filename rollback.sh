#!/bin/bash

# 🔄 SCRIPT DE ROLLBACK D'URGENCE
# Usage: ./rollback.sh

echo ""
echo "⚠️  ROLLBACK D'URGENCE - RETOUR À LA VERSION STABLE"
echo "════════════════════════════════════════════════════════"
echo ""

# Arrêter le serveur
echo "1️⃣  Arrêt du serveur..."
pkill -f "runserver"
sleep 2
echo "   ✅ Serveur arrêté"
echo ""

# Revenir à main
echo "2️⃣  Retour à la branche main..."
git checkout main
echo "   ✅ Branche main activée"
echo ""

# Restaurer la BD
echo "3️⃣  Restauration de la BD originale..."
if [ -f "db.sqlite3.backup" ]; then
    rm db.sqlite3
    cp db.sqlite3.backup db.sqlite3
    echo "   ✅ BD restaurée depuis backup"
else
    echo "   ❌ ERREUR: Backup introuvable!"
    exit 1
fi
echo ""

# Redémarrer le serveur
echo "4️⃣  Redémarrage du serveur en mode production..."
cd /workspaces/given
python3 manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &
sleep 3
echo "   ✅ Serveur relancé"
echo ""

# Vérification
echo "5️⃣  Vérification..."
status=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/)
if [ "$status" = "200" ]; then
    echo "   ✅ Site accessible (HTTP $status)"
else
    echo "   ⚠️  Status HTTP $status"
fi
echo ""

echo "════════════════════════════════════════════════════════"
echo "✅ ROLLBACK COMPLET - RETOUR À LA VERSION STABLE"
echo ""
echo "📌 Branche: main"
echo "📌 BD: restaurée"
echo "📌 Serveur: relancé"
echo "════════════════════════════════════════════════════════"
echo ""
