from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Profile
from teams.models import Team

User = get_user_model()

class LeaderboardTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="testuser1", password="password")
        self.user2 = User.objects.create_user(username="testuser2", password="password")
        self.admin_user = User.objects.create_user(username="adminuser", password="password", is_superuser=True)

        self.profile1, created = Profile.objects.get_or_create(user=self.user1)
        self.profile1.points = 100
        self.profile1.save()

        self.profile2, created = Profile.objects.get_or_create(user=self.user2)
        self.profile2.points = 200
        self.profile2.save()

        self.team1 = Team.objects.create(name="Team A", points=1000, admin=self.admin_user)
        self.team2 = Team.objects.create(name="Team B", points=500, admin=self.admin_user)

    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()
    
    def test_user_leaderboard(self):
        response = self.client.get(reverse('user_leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaderboard/user_leaderboard.html')

        users = list(response.context['ranked_profile_list'])
        self.assertEqual(users[0], self.profile2)
        self.assertEqual(users[1], self.profile1)

    def test_team_leaderboard(self):
        response = self.client.get(reverse('team_leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaderboard/team_leaderboard.html')

        teams = list(response.context['team_list'])
        self.assertEqual(teams[0], self.team1)
        self.assertEqual(teams[1], self.team2)
    
    def test_empty_user_leaderboard(self):
        Profile.objects.all().delete()
        User.objects.all().delete()
        response = self.client.get(reverse('user_leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No users available.")
    
    def test_empty_team_leaderboard(self):
        Team.objects.all().delete()
        response = self.client.get(reverse('team_leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No teams available.")
