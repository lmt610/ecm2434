# Generated by Django 5.1.6 on 2025-03-07 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('race', '0011_alter_raceentry_end_time_alter_raceentry_name_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LeaderboardEntry',
        ),
    ]
