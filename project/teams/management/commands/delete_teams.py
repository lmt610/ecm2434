from django.core.management.base import BaseCommand
from teams.models import Team

class Command(BaseCommand):
    help = "Deletes all teams from the database"

    def handle(self, *args, **kwargs):
        team_no = Team.objects.count()
        Team.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {team_no} teams."))
