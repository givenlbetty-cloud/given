#!/usr/bin/env bash
set -o errexit

echo "=== ATJ Beta - Démarrage ==="

# Nettoyer l'historique des migrations formations (refonte LMS)
python manage.py shell < reset_formations_migrations.py

# Appliquer les migrations
python manage.py migrate --no-input

# Démarrer Gunicorn
gunicorn atj_site.wsgi:application