# Generated by Django 5.1.6 on 2025-03-22 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('race', '0016_merge_20250322_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raceentry',
            name='rank',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
