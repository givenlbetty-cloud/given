"""
WSGI config for atj_site project.

Applique les migrations et crée le Site(id=1) AVANT que Gunicorn
n'accepte des requêtes. C'est le SEUL moment où PostgreSQL est
accessible et où les tables n'ont pas encore été lues.
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atj_site.settings")

# Initialiser Django AVANT get_wsgi_application() pour pouvoir
# exécuter migrate sur PostgreSQL (DATABASE_URL dispo au runtime)
import django
django.setup()

from django.core.management import call_command
from django.contrib.sites.models import Site

# Appliquer les migrations sur PostgreSQL (idempotent)
call_command('migrate', '--no-input')

# Créer le Site id=1 requis par django.contrib.sites + django-allauth
Site.objects.get_or_create(
    id=1,
    defaults={
        'domain': os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'atj-beta.onrender.com'),
        'name': 'ATJ',
    }
)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()