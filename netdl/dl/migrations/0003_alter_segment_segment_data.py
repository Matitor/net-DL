# Generated by Django 5.0.2 on 2024-03-05 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0002_rename_segment_segment_segment_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segment',
            name='segment_data',
            field=models.BinaryField(editable=True),
        ),
    ]