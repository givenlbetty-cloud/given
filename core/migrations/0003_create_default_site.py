# Migration qui crée le Site (id=1) requis par django.contrib.sites + allauth
# Placée dans core/migrations/ car core est dans INSTALLED_APPS
from django.db import migrations


def create_default_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    # Supprimer d'abord tout Site existant avec id=1 pour éviter les conflits
    Site.objects.using(schema_editor.connection.alias).filter(id=1).delete()
    Site.objects.using(schema_editor.connection.alias).create(
        id=1,
        domain='atj-beta.onrender.com',
        name='ATJ',
    )


def remove_default_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.using(schema_editor.connection.alias).filter(id=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),  # Garantit que la table django_site existe
        ('core', '0002_sitesettings_about_description_and_more'),
    ]

    operations = [
        migrations.RunPython(create_default_site, remove_default_site),
    ]