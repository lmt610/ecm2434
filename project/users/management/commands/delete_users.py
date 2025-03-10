from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from race.models import RaceEntry

class Command(BaseCommand):
    help = "Deletes users."

    def handle(self, *args, **kwargs):
        race_entries_to_delete = RaceEntry.objects.filter(user__is_superuser=False)
        num_deleted_race_entries, _ = race_entries_to_delete.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {num_deleted_race_entries} race entries"))

        users_to_delete = User.objects.filter(is_superuser=False)
        num_deleted_users, _ = users_to_delete.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {num_deleted_users} users."))

        self.stdout.write(self.style.SUCCESS("All users and their associated data have been deleted"))

