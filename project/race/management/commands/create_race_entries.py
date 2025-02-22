from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from race.models import Race, Location, LeaderboardEntry
from django.utils import timezone  

class Command(BaseCommand):
    help = "Creates a race entries and users"

    def handle(self, *args, **kwargs):
        # create locations
        start_location1, created = Location.objects.get_or_create(name="Start Point Race 1", latitude=32.8, longitude=35.4)
        end_location1, created = Location.objects.get_or_create(name="End Point Race 2", latitude=33.3, longitude=36.2)

        start_location2, created = Location.objects.get_or_create(name="Start Point Race 2", latitude=20.5, longitude=106.41)
        end_location2, created = Location.objects.get_or_create(name="End Point Race 2", latitude=51.5, longitude=0.1)

        # create races
        race1, created = Race.objects.get_or_create(
            title="Race1",
            start=start_location1,
            end=end_location1,
            start_time=timezone.now(),  
            end_time=timezone.now() + timezone.timedelta(hours=1),   
            is_complete=False,          
        )

        self.stdout.write(self.style.SUCCESS(f"Race '{race1.title}' created or retrieved."))

        race2, created = Race.objects.get_or_create(
            title="Race2",
            start=start_location2,
            end=end_location2,
            start_time=timezone.now(),  
            end_time=timezone.now() + timezone.timedelta(hours=2),   
            is_complete=False,           
        )
        self.stdout.write(self.style.SUCCESS(f"Race '{race2.title}' created or retrieved."))

        # create users
        user1, created = User.objects.get_or_create(username="user1")
        if created:
            user1.set_password("password1")
            user1.save()
            self.stdout.write(self.style.SUCCESS(f"User 'user1' created."))
        else:
            self.stdout.write(self.style.WARNING(f"User 'user1' already exists."))

        user2, created = User.objects.get_or_create(username="user2")
        if created:
            user2.set_password("password2")
            user2.save()
            self.stdout.write(self.style.SUCCESS(f"User 'user2' created."))
        else:
            self.stdout.write(self.style.WARNING(f"User 'user2' already exists."))

        user3, created = User.objects.get_or_create(username="user3")
        if created:
            user3.set_password("password3")
            user3.save()
            self.stdout.write(self.style.SUCCESS(f"User 'user3' created."))
        else:
            self.stdout.write(self.style.WARNING(f"User 'user3' already exists."))

        user4, created = User.objects.get_or_create(username="user4")
        if created:
            user4.set_password("password4")
            user4.save()
            self.stdout.write(self.style.SUCCESS(f"User 'user4' created."))
        else:
            self.stdout.write(self.style.WARNING(f"User 'user4' already exists."))

        # create leaderboard entries
        try:
            # user2 in race1
            leaderboard_entry2 = LeaderboardEntry.objects.create(
                user=user2,
                race=race1,
                completion_time=6000,
            )
            self.stdout.write(self.style.SUCCESS(f"Leaderboard entry created for {user2.username} in {race1.title}"))

            # user3 in race1
            leaderboard_entry3 = LeaderboardEntry.objects.create(
                user=user3,
                race=race1,
                completion_time=5500, 
            )
            self.stdout.write(self.style.SUCCESS(f"Leaderboard entry created for {user3.username} in {race1.title}"))

            # user1 in race2
            leaderboard_entry1 = LeaderboardEntry.objects.create(
                user=user1,
                race=race2,
                completion_time=7500,
            )
            self.stdout.write(self.style.SUCCESS(f"Leaderboard entry created for {user1.username} in {race2.title}"))

            # user4 in race2
            leaderboard_entry4 = LeaderboardEntry.objects.create(
                user=user4,
                race=race2,
                completion_time=8000,
            )
            self.stdout.write(self.style.SUCCESS(f"Leaderboard entry created for {user4.username} in {race2.title}"))
  
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f"ValueError during LeaderboardEntry creation: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))

        self.stdout.write(self.style.SUCCESS("Race and users have been created!"))
