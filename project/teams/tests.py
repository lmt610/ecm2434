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

    def test_team_detail_view_pending(self):
        team = Team.objects.create(name='Team A', admin=self.admin_user)
        TeamJoinRequest.objects.create(team=team, user=self.user)
        response = self.client.get(reverse('team_detail', args=[team.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['join_request_pending'])

    def test_request_join_team(self):
        team = Team.objects.create(name='Team A', admin=self.admin_user)
        response = self.client.get(reverse('request_join_team', args=[team.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TeamJoinRequest.objects.filter(team=team, user=self.user).exists())
        self.assertIn("Your request to join this team has been submitted.", [m.message for m in response.wsgi_request._messages])

    def test_request_join_team_already_member(self):
        team = Team.objects.create(name='Team A', admin=self.admin_user)
        team.members.add(self.user)
        response = self.client.get(reverse('request_join_team', args=[team.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TeamJoinRequest.objects.filter(team=team, user=self.user).exists())
        self.assertIn("You are a member of this team.", [m.message for m in response.wsgi_request._messages])

    def test_request_join_team_already_requested(self):
        team = Team.objects.create(name='Team A', admin=self.admin_user)
        TeamJoinRequest.objects.create(team=team, user=self.user)
        response = self.client.get(reverse('request_join_team', args=[team.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TeamJoinRequest.objects.filter(team=team, user=self.user).count(), 1)
        self.assertIn("You have requested to join this team.", [m.message for m in response.wsgi_request._messages])

    def test_team_join_requests_view(self):
        team = Team.objects.create(name='Team A', admin=self.admin_user)
        TeamJoinRequest.objects.create(team=team, user=self.user)
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('team_join_requests', args=[team.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['join_requests']), 1)
        self.assertEqual(response.context['team'], team)

    def test_team_join_requests_view_no_permission(self):
        team = Team.objects.create(name='Team A', admin=self.admin_user)
        response = self.client.get(reverse('team_join_requests', args=[team.pk]))
        self.assertEqual(response.status_code, 404) 

    def test_approve_join_request(self):
        team = Team.objects.create(name='Team A', admin=self.admin_user)
        join_request = TeamJoinRequest.objects.create(team=team, user=self.user)
        self.client.force_login(self.admin_user)
        response = self.client.post(reverse('approve_join_request', args=[team.pk, join_request.pk]))
        self.assertEqual(response.status_code, 302)
        join_request.refresh_from_db()
        self.assertEqual(join_request.status, 'approved')
        self.assertTrue(team.members.filter(id=self.user.id).exists())
        self.assertIn(f"{self.user.username} has been added to the team.", [m.message for m in response.wsgi_request._messages])

    def test_reject_join_request(self):
        team = Team.objects.create(name='Team A', admin=self.admin_user)
        join_request = TeamJoinRequest.objects.create(team=team, user=self.user)
        self.client.force_login(self.admin_user)
        response = self.client.post(reverse('reject_join_request', args=[team.pk, join_request.pk]))
        self.assertEqual(response.status_code, 302)
        join_request.refresh_from_db()
        self.assertEqual(join_request.status, 'rejected')
        self.assertFalse(team.members.filter(id=self.user.id).exists())
        self.assertIn(f"Join request from {self.user.username} has been rejected.", [m.message for m in response.wsgi_request._messages])

    """def test_leaderboard_view(self):
        team1 = Team.objects.create(name='Team A', admin=self.admin_user, points=100)
        team2 = Team.objects.create(name='Team B', admin=self.admin_user, points=50)
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['teams']), [team1, team2])

    def test_leaderboard_view_empty(self):
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['teams']), 0)"""
    
    def test_model_team_str(self):
        team = Team.objects.create(name='Test Team', admin=self.admin_user)
        self.assertEqual(str(team), 'Test Team')

    def test_model_teamjoinrequest_str(self):
        team = Team.objects.create(name='Test Team', admin=self.admin_user)
        join_request = TeamJoinRequest.objects.create(team=team, user=self.user)
        self.assertEqual(str(join_request), f'Join request for {self.user.username} to {team.name}')
