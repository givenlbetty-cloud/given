from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "core"

    def ready(self):
        # Garantit que le Site (id=1) existe pour django.contrib.sites + allauth
        # AppConfig.ready() est le point d'entrée standard Django, fiable avec gunicorn
        from django.contrib.sites.models import Site
        Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': 'atj-beta.onrender.com',
                'name': 'ATJ',
            }
        )
