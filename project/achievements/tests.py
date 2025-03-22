from django.test import TestCase
from .models import Achievement
from race.models import RaceEntry, Race, Location
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User

class AchievementTests(TestCase):
    def setUp(self):
        # Create test Race objects 
        loc_forum = Location.objects.create(name="Forum (North)", latitude=50.735836, longitude=-3.533852)
        loc_armory = Location.objects.create(name="Armory (A)", latitude=50.736859, longitude=-3.531877)
        loc_comm_gardens = Location.objects.create(name="Community Gardens", latitude=50.740448, longitude=-3.529612)
        loc_reed_pond = Location.objects.create(name="Reed Pond", latitude=50.733950, longitude=-3.537296)

        self.race1 = Race.objects.create(title="Race 1", start=loc_forum, end=loc_armory, medal_requirements=[100,200,300], tags=["funky"]) #distance=0.1
        self.race2 = Race.objects.create(title="Race 2", start=loc_forum, end=loc_comm_gardens, medal_requirements=[100,200,300], tags=["funky", "cool"]) #distance=0.55
        self.race3 = Race.objects.create(title="Race 3", start=loc_reed_pond, end=loc_comm_gardens, medal_requirements=[100,200,300], tags=["water"]) #distance=0.9

        self.user1 = User.objects.create_user(username='testuser1', password='password1')
        self.user2 = User.objects.create_user(username='testuser2', password='password2')

    def test_get_all_user_achievements(self):
        achievement1 = Achievement.objects.create(
            title="A Whole New World",
            description="Run a Race",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
            subconditions=[]
        )
        achievement2 = Achievement.objects.create(
            title="Run two races",
            description="Run two races description",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="1",
            subconditions=[]
        )
        achievement3 = Achievement.objects.create(
            title="Gold Collector",
            description="Get 2 gold medals",
            main_condition_model="COUNT_RACES",
            main_condition_operator="=",
            main_condition_value="2",
            subconditions=[
                ["medal", "=", "Gold"]
            ]
        )
        
        RaceEntry.objects.create(
            race=self.race1,
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=1000)
        )
        query1 = Achievement.get_all_user_achievements(self.user1)
        self.assertEqual(query1.count(), 1)
        self.assertIn(achievement1, query1) 
        
        # add a second race entry (now achievement 1 and 2 are complete)
        RaceEntry.objects.create(
            race=self.race2,
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=1000)
        )
        query2 = Achievement.get_all_user_achievements(self.user1)
        self.assertEqual(query2.count(), 2)
        self.assertIn(achievement1, query2)
        self.assertIn(achievement2, query2)

        # add a race entry for another use (still achievement 1 and 2 are complete)
        RaceEntry.objects.create(
            race=self.race2,
            user=self.user2,
            start_time = now(),
            end_time = now()+timedelta(seconds=3)
        )
        query3 = Achievement.get_all_user_achievements(self.user1)
        self.assertEqual(query2.count(), 2)
        self.assertIn(achievement1, query2)
        self.assertIn(achievement2, query2)

        # make the other user complete all 3 achievements
        RaceEntry.objects.create(
            race=self.race3,
            user=self.user2,
            start_time = now(),
            end_time = now()+timedelta(seconds=4)
        )
        query4 = Achievement.get_all_user_achievements(self.user1)
        self.assertEqual(query2.count(), 2)
        self.assertIn(achievement1, query4)
        self.assertIn(achievement2, query4)
        

    def test_medal_field(self):
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
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=90)
        )
        self.assertFalse(achievement.has_user_completed(self.user1))
        
        # add a silver entry
        RaceEntry.objects.create(
            race=self.race2,
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=125)
        )
        self.assertFalse(achievement.has_user_completed(self.user1))

        # add a gold entry
        RaceEntry.objects.create(
            race=self.race3,
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=50)
        )
        self.assertTrue(achievement.has_user_completed(self.user1))

    # checks that achievements works for the 'duration' field
    def test_duration_field(self):
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
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=50)
        )
        self.assertFalse(achievement.has_user_completed(self.user1))
        
        # add a silver entry
        RaceEntry.objects.create(
            race=self.race2,
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=125)
        )
        self.assertFalse(achievement.has_user_completed(self.user1))

        # add a gold entry
        RaceEntry.objects.create(
            race=self.race3,
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=45)
        )
        self.assertTrue(achievement.has_user_completed(self.user1))

    # checks that achievements works for the 'distance' field
    def test_distance_field(self):
        achievement = Achievement.objects.create(
            title="The Long Game",
            description="Complete 2 races with a distance over 0.5km",
            main_condition_model="COUNT_RACES",
            main_condition_operator="=",
            main_condition_value="2",
            subconditions=[
                ["distance", ">", "0.5"]
            ]
        )
        # add a short race
        RaceEntry.objects.create(
            race=self.race1,
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=50)
        )
        self.assertFalse(achievement.has_user_completed(self.user1))
        
        # add a long race
        RaceEntry.objects.create(
            race=self.race2,
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=125)
        )
        self.assertFalse(achievement.has_user_completed(self.user1))

        # add a long race
        RaceEntry.objects.create(
            race=self.race3,
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=45)
        )
        self.assertTrue(achievement.has_user_completed(self.user1))

    def test_position_field(self):
        achievement = Achievement.objects.create(
            title="Double Crown",
            description="Hold the top leaderboard position on two races",
            main_condition_model="COUNT_RACES",
            main_condition_operator="=",
            main_condition_value="2",
            subconditions=[
                ["position", "=", "1"]
            ]
        )
        # add one race where the user holds the top spot
        RaceEntry.objects.create(
            race=self.race1,
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=90)
        )
        RaceEntry.objects.create(
            race=self.race1,
            user=self.user2,
            start_time = now(),
            end_time = now()+timedelta(seconds=120)
        )
        self.assertFalse(achievement.has_user_completed(self.user1))
        
        # add a race where the user is in 2nd
        RaceEntry.objects.create(
            race=self.race2,
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=125)
        )
        RaceEntry.objects.create(
            race=self.race2,
            user=self.user2,
            start_time = now(),
            end_time = now()+timedelta(seconds=90)
        )
        self.assertFalse(achievement.has_user_completed(self.user1))

        # add a race where the user is 1st
        RaceEntry.objects.create(
            race=self.race3,
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=50)
        )
        RaceEntry.objects.create(
            race=self.race3,
            user=self.user2,
            start_time = now(),
            end_time = now()+timedelta(seconds=90)
        )
        self.assertTrue(achievement.has_user_completed(self.user1))

    def test_tags_field(self):
        achievement = Achievement.objects.create(
            title="TEST - funky town",
            description="Complete two funky races",
            main_condition_model="COUNT_RACES",
            main_condition_operator="=",
            main_condition_value="2",
            subconditions=[
                ["tags", "contains", "funky"]
            ]
        )
        # complete a funky race
        RaceEntry.objects.create(
            race=self.race1,
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=100)
        )
        self.assertFalse(achievement.has_user_completed(self.user1))

        # complete a non-funky race
        RaceEntry.objects.create(
            race=self.race3,
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=100)
        )
        self.assertFalse(achievement.has_user_completed(self.user1))

        # complete the final funky race to get the achievement
        RaceEntry.objects.create(
            race=self.race2,
            user=self.user1,
            start_time = now(),
            end_time = now()+timedelta(seconds=50)
        )
        self.assertTrue(achievement.has_user_completed(self.user1))

