# Generated by Django 4.2.20 on 2025-03-24 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_profile_streak'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='streak',
        ),
    ]
