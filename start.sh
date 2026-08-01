#!/usr/bin/env bash
set -o errexit

# Migrate sur PostgreSQL
python manage.py migrate --no-input

# Démarrer Gunicorn
gunicorn atj_site.wsgi:application