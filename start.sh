#!/usr/bin/env bash
set -o errexit

echo "=== ATJ Beta - Démarrage ==="

# 1. Supprimer les anciennes tables formations (refonte LMS)
echo "Suppression des anciennes tables formations..."
python -c "
import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atj_site.settings')
import django; django.setup()
from django.db import connection
with connection.cursor() as c:
    c.execute('DROP TABLE IF EXISTS formations_formation, formations_lecon, formations_session, formations_inscription, formations_paiement CASCADE')
    c.execute(\"DELETE FROM django_migrations WHERE app = 'formations'\")
print('Anciennes tables et historique supprimés')
"

# 2. Appliquer les migrations
echo "Application des migrations..."
python manage.py migrate --no-input

# 3. Démarrer Gunicorn
echo "Démarrage Gunicorn..."
gunicorn atj_site.wsgi:application