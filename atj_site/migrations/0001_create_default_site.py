from django.db import migrations


def create_default_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.using(schema_editor.connection.alias).get_or_create(
        id=1,
        defaults={
            'domain': 'atj-beta.onrender.com',
            'name': 'ATJ'
        }
    )


class Migration(migrations.Migration):
    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]
    operations = [
        migrations.RunPython(create_default_site),
    ]