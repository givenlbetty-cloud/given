#!/usr/bin/env bash
set -o errexit

# Migrate sur PostgreSQL (accessible uniquement au runtime sur Render)
python manage.py migrate --no-input

# Créer le Site id=1 requis par django.contrib.sites + allauth
python manage.py shell -c "from django.contrib.sites.models import Site; Site.objects.filter(id=1).delete(); Site.objects.create(id=1, domain='atj-beta.onrender.com', name='ATJ'); print('Site id=1 created')"

# Démarrer Gunicorn
gunicorn atj_site.wsgi:application