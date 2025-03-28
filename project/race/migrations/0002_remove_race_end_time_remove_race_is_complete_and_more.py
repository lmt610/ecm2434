# Generated by Django 4.2.19 on 2025-02-22 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('race', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='race',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='race',
            name='is_complete',
        ),
        migrations.RemoveField(
            model_name='race',
            name='start_time',
        ),
        migrations.CreateModel(
            name='RaceEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('is_complete', models.BooleanField()),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='race.race')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
