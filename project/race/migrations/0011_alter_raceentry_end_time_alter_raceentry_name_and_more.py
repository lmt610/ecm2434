# Generated by Django 5.1.6 on 2025-03-07 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('race', '0010_remove_raceentry_is_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raceentry',
            name='end_time',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='raceentry',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='raceentry',
            name='start_time',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
