from django.test import TestCase
from .models import Achievement
from race.models import RaceEntry, Race, Location
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User

class AchievementTests(TestCase):
    def setUp(self):
        # Create test Race objects 
        loc1 = Location.objects.create(name="Forum (North)", latitude=50.735836, longitude=-3.533852)
        loc2 = Location.objects.create(name="Armory (A)", latitude=50.736859, longitude=-3.531877)
        self.race1 = Race.objects.create(title="Race 1", start=loc1, end=loc2, medal_requirements=[100,200,300])
        self.race2 = Race.objects.create(title="Race 2", start=loc1, end=loc2, medal_requirements=[100,200,300])
        self.race3 = Race.objects.create(title="Race 3", start=loc1, end=loc2, medal_requirements=[100,200,300])

        # User needed for authorised get request 
        self.user = User.objects.create_user(username='testuser', password='password')

        
    def test_single_subcondition(self):
        achievement = Achievement.objects.create(
            title="Gold Collector",
            description="Get 2 gold medals",
            main_condition_model="COUNT_RACES",
            main_condition_operator="=",
            main_condition_value="2",
            subconditions=[
                ["medal", "=", "Gold"]
            ]
        )
        # add a single gold medal entry
        RaceEntry.objects.create(
            race=self.race1,
            user=self.user,
            start_time = now(),
            end_time = now()+timedelta(seconds=90)
        )
        self.assertFalse(achievement.has_user_completed(self.user))
        
        # add a silver entry
        RaceEntry.objects.create(
            race=self.race2,
            user=self.user,
            start_time = now(),
            end_time = now()+timedelta(seconds=125)
        )
        self.assertFalse(achievement.has_user_completed(self.user))

        # add a gold entry
        RaceEntry.objects.create(
            race=self.race3,
            user=self.user,
            start_time = now(),
            end_time = now()+timedelta(seconds=50)
        )
        self.assertTrue(achievement.has_user_completed(self.user))

    # checks that achievements works for fields that are derived from other attributes
    # in this case the duration of a race entry
    def test_derived_field_subcondition(self):
        achievement = Achievement.objects.create(
            title="Sprinter",
            description="Complete 2 races in under 1 minute",
            main_condition_model="COUNT_RACES",
            main_condition_operator="=",
            main_condition_value="2",
            subconditions=[
                ["duration", "<", "60"]
            ]
        )
        # add a single gold medal entry
        RaceEntry.objects.create(
            race=self.race1,
            user=self.user,
            start_time = now(),
            end_time = now()+timedelta(seconds=50)
        )
        self.assertFalse(achievement.has_user_completed(self.user))
        
        # add a silver entry
        RaceEntry.objects.create(
            race=self.race2,
            user=self.user,
            start_time = now(),
            end_time = now()+timedelta(seconds=125)
        )
        self.assertFalse(achievement.has_user_completed(self.user))

        # add a gold entry
        RaceEntry.objects.create(
            race=self.race3,
            user=self.user,
            start_time = now(),
            end_time = now()+timedelta(seconds=45)
        )
        self.assertTrue(achievement.has_user_completed(self.user))

