"""
WSGI config for atj_site project.
Exécute le nettoyage et les migrations au démarrage de Gunicorn.
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atj_site.settings")

import django
django.setup()

# Repeupler automatiquement les formations au démarrage (Render)
from django.core.management import call_command
try:
    call_command('populate_formations')
except Exception:
    pass

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
