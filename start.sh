#!/usr/bin/env bash
set -o errexit

echo "=== ATJ Beta - Démarrage ==="

# 1. Nettoyer l'historique formations pour la refonte LMS (via shell inline)
echo "Nettoyage historique migrations formations..."
python -c "
import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atj_site.settings')
import django; django.setup()
from django.db import connection
with connection.cursor() as c:
    c.execute(\"DELETE FROM django_migrations WHERE app = 'formations'\")
print('OK')
"

# 2. Appliquer les migrations
echo "Application des migrations..."
python manage.py migrate --no-input

# 3. Démarrer Gunicorn
echo "Démarrage Gunicorn..."
gunicorn atj_site.wsgi:application