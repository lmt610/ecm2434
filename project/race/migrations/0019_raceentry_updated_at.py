# Generated by Django 4.2.11 on 2025-03-22 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('race', '0018_merge_0014_race_tags_0017_alter_raceentry_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='raceentry',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
