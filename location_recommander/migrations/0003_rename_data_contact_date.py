# Generated by Django 5.0.6 on 2024-05-29 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location_recommander', '0002_predicited_areamap'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='data',
            new_name='date',
        ),
    ]
