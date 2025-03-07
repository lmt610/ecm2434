from django.core.management.base import BaseCommand
from race.models import Race, Location, RaceEntry

class Command(BaseCommand):
    help = "Deletes all races."

    def handle(self, *args, **kwargs):
        num_deleted_leaderboard, _ = RaceEntry.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {num_deleted_leaderboard} race entries."))

        num_deleted_races, _ = Race.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {num_deleted_races} races."))

        num_deleted_locations, _ = Location.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {num_deleted_locations} locations."))

        self.stdout.write(self.style.SUCCESS("All races have been deleted"))
