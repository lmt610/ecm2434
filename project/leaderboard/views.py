from django.shortcuts import render
from users.models import Profile
from teams.models import Team

def user_leaderboard(request):
    user_list = Profile.objects.select_related('user').order_by('-points')[:10]
    return render(request, 'leaderboard/user_leaderboard.html', {'user_list': user_list})

def team_leaderboard(request):
    team_list = Team.objects.all().order_by('-points')[:10]
    return render(request, 'leaderboard/team_leaderboard.html', {'team_list': team_list})



