# Generated by Django 5.1.6 on 2025-03-20 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('race', '0014_remove_raceentry_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='raceentry',
            name='rank',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
