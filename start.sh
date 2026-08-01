#!/usr/bin/env bash
set -o errexit

echo "=== ATJ Beta - Démarrage ==="

# Nettoyer l'historique des migrations formations (refonte LMS)
echo "Nettoyage historique migrations formations..."
python manage.py shell -c "
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute(\"DELETE FROM django_migrations WHERE app = 'formations'\")
print('Historique formations effacé')
"

# Appliquer les migrations
echo "Application des migrations..."
python manage.py migrate --no-input

# Démarrer Gunicorn
echo "Démarrage Gunicorn..."
gunicorn atj_site.wsgi:application