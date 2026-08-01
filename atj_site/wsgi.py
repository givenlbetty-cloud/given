"""
WSGI config for atj_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atj_site.settings")

application = get_wsgi_application()

# Garantit que le Site (id=1) existe pour django.contrib.sites + allauth
# Exécuté à chaque démarrage du worker, pas seulement au build
from django.contrib.sites.models import Site
Site.objects.get_or_create(
    id=1,
    defaults={
        'domain': os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'atj-beta.onrender.com'),
        'name': 'ATJ',
    }
)
