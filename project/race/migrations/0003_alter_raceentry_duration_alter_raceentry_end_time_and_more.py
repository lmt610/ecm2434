# Generated by Django 4.2.19 on 2025-02-22 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('race', '0002_remove_race_end_time_remove_race_is_complete_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raceentry',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='raceentry',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='raceentry',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
