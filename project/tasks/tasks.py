from django.core.management.base import BaseCommand
from .models import Task

class Command(BaseCommand):
    help = 'Create initial tasks'

    def handle(self, *args, **options):
        tasks = [
            {'title': 'Complete tutorial', 'points_reward': 5, 'link_text': 'Complete Tutorial', 'link_url': '/tutorial/'},
            {'title': 'Participate in forum', 'points_reward': 10, 'link_text': 'Participate in Forum', 'link_url': '/forum/'},
            {'title': 'Refer a friend', 'points_reward': 20, 'link_text': 'Refer a Friend', 'link_url': '/refer/'},
        ]

        for task in tasks:
            Task.objects.create(**task)
