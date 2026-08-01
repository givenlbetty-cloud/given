import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atj_site.settings')
django.setup()

from django.contrib.sites.models import Site

site, created = Site.objects.get_or_create(
    id=1,
    defaults={
        'domain': os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'atj-beta.onrender.com'),
        'name': 'ATJ'
    }
)

if created:
    print(f'✅ Site créé: {site.domain} (id=1)')
else:
    print(f'✅ Site existant: {site.domain} (id=1)')
    # Mettre à jour le domaine si changé
    expected_domain = os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'atj-beta.onrender.com')
    if site.domain != expected_domain:
        site.domain = expected_domain
        site.save()
        print(f'   Domaine mis à jour: {site.domain}')