"""
WSGI config for atj_site project.
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atj_site.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()