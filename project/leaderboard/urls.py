from django.urls import path
from .views import user_leaderboard, team_leaderboard

urlpatterns = [
    path('user/', user_leaderboard, name='user_leaderboard'),
    path('team/', team_leaderboard, name='team_leaderboard'),
]