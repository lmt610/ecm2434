from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from race.models import Race, Location
from leaderboard.models import LeaderboardEntry
from django.utils import timezone  

class Command(BaseCommand):
    help = "Deletes all races."

    def handle(self, *args, **kwargs):
        num_deleted_leaderboard, _ = LeaderboardEntry.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {num_deleted_leaderboard} leaderboard entries."))

        num_deleted_races, _ = Race.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {num_deleted_races} races."))

        num_deleted_locations, _ = Location.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {num_deleted_locations} locations."))

        self.stdout.write(self.style.SUCCESS("All races have been deleted"))
