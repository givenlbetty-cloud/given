"""
WSGI config for atj_site project.
Exécute le nettoyage et les migrations au démarrage de Gunicorn.
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atj_site.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
