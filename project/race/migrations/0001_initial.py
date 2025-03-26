# Generated by Django 5.1.6 on 2025-03-26 10:59

import django.db.models.deletion
import race.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('medal_requirements', models.JSONField(default=list, validators=[race.models.validate_ascending_three_items])),
                ('tags', models.JSONField(default=list, validators=[race.models.validate_list_of_strings])),
                ('end', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='end_races', to='race.location')),
                ('start', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start_races', to='race.location')),
            ],
        ),
        migrations.CreateModel(
            name='RaceEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('start_time', models.DateTimeField(blank=True, default=None, null=True)),
                ('end_time', models.DateTimeField(blank=True, default=None, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('medal', models.CharField(default='None', max_length=6)),
                ('num_completions', models.IntegerField(default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='race.race')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Streak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_streak', models.IntegerField(default=0)),
                ('longest_streak', models.IntegerField(default=0)),
                ('date_of_last_race', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
