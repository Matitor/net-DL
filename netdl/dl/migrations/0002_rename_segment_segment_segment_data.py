# Generated by Django 5.0.2 on 2024-03-05 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='segment',
            old_name='segment',
            new_name='segment_data',
        ),
    ]
