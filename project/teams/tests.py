from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Team, TeamJoinRequest
from .forms import TeamForm  

class TeamTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.admin_user = User.objects.create_user(username='adminuser', password='password', is_superuser=True) 
        self.client.force_login(self.user)

    def test_team_list_view(self):
        team1 = Team.objects.create(name='Team A', admin=self.admin_user)
        team2 = Team.objects.create(name='Team B', admin=self.admin_user)
        response = self.client.get(reverse('team_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(team1.name, str(response.content))
        self.assertIn(team2.name, str(response.content))
        self.assertEqual(len(response.context['teams']), 2)

    def test_team_detail_view(self):
        team = Team.objects.create(name='Team A', admin=self.admin_user)
        response = self.client.get(reverse('team_detail', args=[team.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['team'], team)
        self.assertFalse(response.context['has_joined'])
        self.assertFalse(response.context['join_request_pending'])

    def test_team_detail_view_with_membership(self):
        team = Team.objects.create(name='Team A', admin=self.admin_user)
        team.members.add(self.user)
        response = self.client.get(reverse('team_detail', args=[team.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['has_joined'])
