from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from race.models import Race, Location, LeaderboardEntry
from django.utils import timezone  

class Command(BaseCommand):
    help = "Deletes users."

    def handle(self, *args, **kwargs):
        superuser_exists = User.objects.filter(is_superuser=True).exists()
        if superuser_exists:
            users_to_delete = User.objects.filter(is_superuser=False)
            num_deleted_users, _ = users_to_delete.delete()
            self.stdout.write(self.style.SUCCESS(f"Deleted {num_deleted_users} users."))
        else:
            num_deleted_users, _ = User.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"Deleted {num_deleted_users} users."))

        self.stdout.write(self.style.SUCCESS("All users have been deleted"))

