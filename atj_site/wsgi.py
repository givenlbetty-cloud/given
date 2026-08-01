"""
WSGI config for atj_site project.
Exécute le nettoyage et les migrations au démarrage de Gunicorn.
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atj_site.settings")

import django
django.setup()

from django.db import connection
from django.core.management import call_command

# Nettoyer les anciennes tables formations (refonte LMS)
with connection.cursor() as c:
    c.execute("DROP TABLE IF EXISTS formations_formation, formations_lecon, formations_session, formations_inscription, formations_paiement CASCADE")
    c.execute("DELETE FROM django_migrations WHERE app = 'formations'")

# Appliquer les migrations
call_command('migrate', '--no-input')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
