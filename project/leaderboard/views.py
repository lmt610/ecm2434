from django.shortcuts import render
from users.models import Profile
from teams.models import Team
from race.models import RaceEntry
from django.db.models import F, ExpressionWrapper, DurationField

def user_leaderboard(request):
    user_list = Profile.objects.select_related('user').order_by('-points')[:10]
    return render(request, 'leaderboard/user_leaderboard.html', {'user_list': user_list})

def team_leaderboard(request):
    team_list = Team.objects.all().order_by('-points')[:10]
    return render(request, 'leaderboard/team_leaderboard.html', {'team_list': team_list})

def race_leaderboard(request):
    race_title = request.GET.get("race_title")
    if race_title:
        race_entries = RaceEntry.objects.filter(race__title__icontains=race_title)
    else:
        race_entries = RaceEntry.objects
    
    ordered_entries = race_entries.annotate(
            duration=ExpressionWrapper(F('end_time')-F('start_time'), output_field=DurationField())
        ).order_by('duration')

    top_entries = ordered_entries.select_related("user", "race")[:10]
    return render(request, 'leaderboard/race_leaderboard.html', {'top_entries':top_entries})



