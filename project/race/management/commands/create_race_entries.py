from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from race.models import Race, Location, RaceEntry
from django.utils.timezone import now, timedelta 

class Command(BaseCommand):
    help = "Creates race entries and users"

    def handle(self, *args, **kwargs):
        start_location1, created = Location.objects.get_or_create(name="Start Point Race 1", latitude=32.8, longitude=35.4)
        end_location1, created = Location.objects.get_or_create(name="End Point Race 1", latitude=33.3, longitude=36.2)

        start_location2, created = Location.objects.get_or_create(name="Start Point Race 2", latitude=20.5, longitude=106.41)
        end_location2, created = Location.objects.get_or_create(name="End Point Race 2", latitude=51.5, longitude=0.1)

        race1, created = Race.objects.get_or_create(
            title="Race 1",
            start=start_location1,
            end=end_location1,
        )

        self.stdout.write(self.style.SUCCESS(f"Race '{race1.title}' created or retrieved."))

        race2, created = Race.objects.get_or_create(
            title="Race 2",
            start=start_location2,
            end=end_location2,
        )
        self.stdout.write(self.style.SUCCESS(f"Race '{race2.title}' created or retrieved."))

        users = ["user1", "user2", "user3", "user4"]
        for user in users:
            user_instance, created = User.objects.get_or_create(username=user)
            if created:
                user_instance.set_password(user)  
                user_instance.save()
                self.stdout.write(self.style.SUCCESS(f"User '{user_instance.username}' created."))
            else:
                self.stdout.write(self.style.WARNING(f"User '{user_instance.username}' already exists."))

        try:
            completion_times = {
                "user2": (race1, 6000),
                "user3": (race1, 5500),
                "user1": (race2, 7500),
                "user4": (race2, 8000),
            }

            for username, (race, completion_time) in completion_times.items():
                user = User.objects.get(username=username)
                RaceEntry.objects.create(
                    user=user,
                    race=race,
                    start_time=now(),
                    end_time=now()+timedelta(seconds=completion_time)
                )
                self.stdout.write(self.style.SUCCESS(f"Race entry created for {user.username} in {race.title}"))

        except ValueError as e:
            self.stdout.write(self.style.ERROR(f"ValueError during RaceEntry creation: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))

        self.stdout.write(self.style.SUCCESS("Race and users have been created!"))
