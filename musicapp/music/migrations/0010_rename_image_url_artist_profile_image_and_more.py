# Generated by Django 5.1.6 on 2025-03-24 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0009_alter_artist_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artist',
            old_name='image_url',
            new_name='profile_image',
        ),
        migrations.AddField(
            model_name='artist',
            name='detail_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
