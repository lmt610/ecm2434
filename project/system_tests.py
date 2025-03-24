from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import UserSettings, Profile
from race.models import Race, Location, RaceEntry
from teams.models import Team, TeamJoinRequest
from tasks.models import Task, UserTaskCompletion
from achievements.models import Achievement
from django.contrib.auth import get_user_model
from django.db import IntegrityError
import datetime
from datetime import timedelta
from django.utils import timezone
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


class SystemTestCase(TestCase):
    """Test cases to validate system behavior like user actions, race completion, team functionality, and leaderboard updates."""

    def setUp(self):
        """
        Set up initial conditions for each test.
        This includes creating necessary objects such as users, teams, races, locations, and achievements.
        """

        # Create a unique user for each test
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        
        # Get the user profile associated with the user, initializing points as 0
        self.user_profile = Profile.objects.get(user=self.user, points=0)  # Get Profile linked to the User

        # Create an admin user 
        self.admin_user = User.objects.create_user(username="admin", password="password", email="admin@test.com")
        self.admin_user.save(using="default")  # Save the admin user instance

        
        # Create a team with the admin user as the admin of the team
        self.team = Team.objects.create(name="Test Team", admin=self.admin_user)

        # Initialize the client and log in the test user
        self.client = Client()
        self.client.login(username="testuser", password="testpassword")

        # Set up race data needed for the tests
        self.start_location = Location.objects.create(latitude=50.738326, longitude=-3.531160) 
        self.end_location = Location.objects.create(latitude=50.735097, longitude=-3.530182)  

        # Create a test race with specific conditions and tags
        self.race = Race.objects.create(
            title="Test Race",
            start=self.start_location,
            end=self.end_location,
            medal_requirements=[150, 180, 300],
            tags=["marathon", "charity"]
        )

        # Set up an achievement associated with completing a race
        self.achievement = Achievement.objects.create(
            title="Test achievement",
            description="Run a Race",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
            subconditions=[]
        )

        self.start_time=datetime.datetime(2025, 3, 24, 14, 30, 0)


    def test_login_api(self):
        """Test if the login API works as expected."""
        # Send login request and check the response status
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Expect redirect after successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)  # Check that user is authenticated

    def test_get_user_leaderboard(self):
        """Test if the user leaderboard page works as expected."""
        # Send a GET request to fetch the leaderboard page
        response = self.client.get(reverse('user_leaderboard'))

        # Check that the page returns a successful response
        self.assertEqual(response.status_code, 200)

        # Check for presence of expected content on the page
        self.assertContains(response, 'leaderboard-list')  # Ensure leaderboard is rendered
        self.assertContains(response, 'user-card')  # Check that user cards are displayed
        self.assertContains(response, 'testuser')  # Check that the test user appears in the leaderboard

    def test_change_password_api(self):
        """Test if the password change API works as expected."""
        # Prepare the form data for password change
        form_data = {
            'old_password': 'testpassword',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        }
        # Send a POST request to change the password
        response = self.client.post(reverse('change_password'), form_data)

        # Check that the password change request was successful
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), "Your password was successfully updated!")

    def test_toggle_user_setting(self):
        """Test toggling a user setting through the API."""
        setting = 'location_tracking'  # Example setting for location tracking
        # Send a POST request to toggle the user setting
        response = self.client.post(reverse('toggle_setting'), {'setting': setting, 'value': 'true'})

        # Ensure the request was successful
        self.assertEqual(response.status_code, 200)
        
        # Retrieve the user's settings and check that the value was updated
        settings = UserSettings.objects.get(user=self.user)
        self.assertTrue(settings.location_tracking)  # Check if location tracking is enabled

    def test_delete_account(self):
        """Test if the delete account API works as expected."""
        # Send a POST request to delete the account
        response = self.client.post(reverse('delete_account'))
        
        # After deletion, expect a redirect (status code 302)
        self.assertEqual(response.status_code, 302)
        
        # Ensure that the user account no longer exists
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_race_achievement_unlocked(self):
        """Test if an achievement is unlocked after completing the first race."""
        # Simulate a race completion (achieving the race condition)
        start_time = self.start_time
        end_time = self.start_time + timedelta(seconds=140)

        # Create a race entry for the user
        race_entry = RaceEntry.objects.create(race=self.race, user=self.user, start_time=start_time, end_time=end_time)

        # Ensure the achievement is unlocked after completing the race
        achievement = Achievement.objects.get(id=self.achievement.id)
        self.assertTrue(achievement.has_user_completed(self.user))  # Check if achievement condition is met

    def test_race_completion_and_medals(self):
        """Test race completion, awarding medals, and leaderboard updates."""
        # Simulate a fast race completion (gold medal time)
        start_time = self.start_time
        end_time = self.start_time + timedelta(seconds=90)  # Time less than gold (150 seconds)

        # Create a race entry for the user with the calculated times
        race_entry = RaceEntry.objects.create(race=self.race, user=self.user, start_time=start_time, end_time=end_time)

        # Ensure the user receives a gold medal
        self.assertEqual(race_entry.medal, 'Gold')  # The user should have earned a gold medal

    def test_race_completion_no_medal(self):
        """Test race completion without a medal due to slow time."""
        # Simulate a slow race completion (no medal)
        start_time = self.start_time
        end_time = self.start_time + timedelta(seconds=310)  # Time exceeds the bronze medal time (300 seconds)

        # Create a race entry for the user with the calculated times
        race_entry = RaceEntry.objects.create(race=self.race, user=self.user, start_time=start_time, end_time=end_time)

        # Ensure the user does not receive any medal
        self.assertEqual(race_entry.medal, 'None')  # No medal due to slow time

    def test_join_team(self):
        """Test if a user can join a team."""
        # Send a request to join the team
        response = self.client.post(reverse('request_join_team', args=[self.team.id]), {'team_id': self.team.id})
        self.assertEqual(response.status_code, 302)  # Expect a redirect after successful request

        # Check that a pending join request is created
        join_request = TeamJoinRequest.objects.filter(team=self.team, user=self.user, status='pending').first()
        self.assertIsNotNone(join_request)  # Ensure join request is in 'pending' state

        # Simulate admin approving the join request
        self.client.force_login(self.team.admin)  # Log in as the admin user
        response = self.client.post(reverse('approve_join_request', args=[self.team.id, join_request.id]))

        # Check if the user was successfully added to the team
        team = Team.objects.get(id=self.team.id)
        self.assertIn(self.user, team.members.all())  # Ensure the user is part of the team

    def test_task_completion_and_leaderboard_update(self):
        """Test task completion and verify that both user and team points are updated."""
        self.team.members.add(self.user)  # Manually add the user to the team

        # Set up the task with points for completion
        task = Task.objects.create(
            title="Test Task",
            race=self.race,
            points_awarded=50,  # Awarding 50 points for task completion
            required_races=1,
            task_type='single',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1)
        )

        # User completes the race and the task
        start_time = self.start_time
        end_time = self.start_time + timedelta(seconds=310)
        race_entry = RaceEntry.objects.create(race=self.race, user=self.user, start_time=start_time, end_time=end_time)


        # Simulate the task completion
        if not UserTaskCompletion.objects.filter(user=self.user, task=task).exists():
            try:
                # Create the task completion entry for the user
                UserTaskCompletion.objects.create(user=self.user, task=task)

            except IntegrityError:
                # Handle potential duplicate task completion entry
                print("Task completion entry already exists.")

        # Verify if user and team's points have been updated
        self.user_profile.refresh_from_db()  # Refresh user profile to get updated points
        self.assertEqual(self.user_profile.points, 75)  # User gets 50 points for task completion, 5 for completing a race, 20 for first place

        # Check if the task was completed successfully
        self.assertTrue(UserTaskCompletion.objects.filter(user=self.user, task=task).exists())

        # Ensure team points have been updated as well
        self.team.refresh_from_db()  # Total points across team members
        self.assertEqual(self.team.points, 75)  # Ensure the team points have updated with the user

        # Check the leaderboard to ensure that both user and team are updated
        response = self.client.get(reverse('user_leaderboard'))
        self.assertContains(response, self.user)  # User should appear in the leaderboard

        response = self.client.get(reverse('team_leaderboard'))
        self.assertContains(response, self.team.name)  # Team should appear in the leaderboard
