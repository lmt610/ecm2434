# Generated by Django 5.1.6 on 2025-02-14 14:31

import django.db.models.deletion
from django.db import migrations, models



class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('is_complete', models.BooleanField()),
                ('end', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='end_races', to='race.location')),
                ('start', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start_races', to='race.location')),
            ],
        ),
    ]
