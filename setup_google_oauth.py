"""
Script de configuration Google OAuth pour ATJ Beta.
Exécutez dans le Render Shell :
    python manage.py shell < setup_google_oauth.py

Ou bien :
    python manage.py shell
    >>> exec(open('setup_google_oauth.py').read())
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atj_site.settings')
import django
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

# === CONFIGURATION ===
# Remplacez par vos vrais identifiants Google Cloud
CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'VOTRE_CLIENT_ID_ICI')
CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', 'VOTRE_CLIENT_SECRET_ICI')

# 1. Créer ou mettre à jour la SocialApp Google
app, created = SocialApp.objects.update_or_create(
    provider='google',
    defaults={
        'name': 'Google',
        'client_id': CLIENT_ID,
        'secret': CLIENT_SECRET,
    }
)

# 2. Lier le Site (id=1) à la SocialApp
site = Site.objects.get(id=1)
app.sites.add(site)

print(f"{'✅ Créé' if created else '✅ Mis à jour'} SocialApp: {app.name}")
print(f"   Client ID: {app.client_id[:20]}...")
print(f"   Site lié: {site.domain} (id={site.id})")