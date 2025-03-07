from django.shortcuts import render
from users.models import Profile
from teams.models import Team
from .models import LeaderboardEntry

def user_leaderboard(request):
    user_list = Profile.objects.select_related('user').order_by('-points')[:10]
    return render(request, 'leaderboard/user_leaderboard.html', {'user_list': user_list})

def team_leaderboard(request):
    team_list = Team.objects.all().order_by('-points')[:10]
    return render(request, 'leaderboard/team_leaderboard.html', {'team_list': team_list})

def race_leaderboard(request):
    race_title = request.GET.get("race_title")
    if race_title:
        leaderboard_entries = LeaderboardEntry.objects.filter(race__title__icontains=race_title).order_by('completion_time').select_related('user', 'race')
    else:
        leaderboard_entries = LeaderboardEntry.objects.order_by('completion_time').select_related('user', 'race')
        
    top_entries = leaderboard_entries[:10]
    entries_count = leaderboard_entries.count()

    context = {
        'top_entries': top_entries,
    }
    return render(request, 'leaderboard/race_leaderboard.html', context)



