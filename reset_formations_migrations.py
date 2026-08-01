"""Nettoie l'historique des migrations formations pour la refonte LMS."""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atj_site.settings')
import django
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DELETE FROM django_migrations WHERE app = 'formations'")
    deleted = cursor.rowcount

print(f"✅ {deleted} enregistrement(s) supprimé(s) de django_migrations (app=formations)")