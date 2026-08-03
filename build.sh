#!/usr/bin/env bash
# exit on error
set -o errexit

# Installer poppler-utils pour pdf2image (couverture auto des livres)
apt-get update -qq && apt-get install -y -qq poppler-utils

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python ensure_site.py
