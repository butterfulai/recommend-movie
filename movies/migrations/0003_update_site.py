from django.db import migrations


def update_site(apps, schema_editor):
    site = apps.get_model('sites', 'Site')
    site.objects.update_or_create(
        id=1,
        defaults={
            'domain': '127.0.0.1:8000',
            'name': 'Movie Recommend',
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('movies', '0002_seed_movies'),
    ]

    operations = [
        migrations.RunPython(update_site, migrations.RunPython.noop),
    ]
