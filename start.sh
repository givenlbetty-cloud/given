#!/usr/bin/env bash
set -o errexit

echo "Applying pending Django migrations..."
python manage.py migrate --no-input

echo "Starting Gunicorn..."
exec gunicorn atj_site.wsgi:application
