from django.shortcuts import render
from users.models import Profile
from teams.models import Team
from django.db.models import F, ExpressionWrapper, DurationField
from django.db.models.functions import Extract
from django.db import models
from race.models import Race, RaceEntry
import logging


def user_leaderboard(request):
    # Fetch all profiles ordered by points
    ranked_profiles = Profile.objects.all().order_by('-points')

    # Get all teams
    teams = Team.objects.all()
    selected_team = request.GET.get('team', 'all')  # Default to 'all' if no team selected


    if selected_team != 'all':
        try:
            # Try to get the selected team
            team = Team.objects.get(name=selected_team)
            team_members = team.members.all()  # Get all members of the selected team

            # Filter profiles based on users in the selected team
            ranked_profiles = ranked_profiles.filter(user__in=team_members)
        except Team.DoesNotExist:
            ranked_profiles = Profile.objects.none()  # No profiles if team doesn't exist

    # Filter out duplicate users (in case the same user is listed multiple times)
    displayed_profiles = set()
    filtered_profiles = []
    for profile in ranked_profiles:
        if profile.user.id not in displayed_profiles:
            filtered_profiles.append(profile)
            displayed_profiles.add(profile.user.id)


    team_ranked_profiles = list(ranked_profiles)  # Create a list to preserve the order
    for index, profile in enumerate(team_ranked_profiles):
        profile.rank_in_team = index + 1  # Rank starts from 1


    # Context for rendering
    context = {
        'ranked_profile_list': team_ranked_profiles,
        'teams': teams,
        'selected_team': selected_team,
    }

    return render(request, 'leaderboard/user_leaderboard.html', context)


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
    ordered_entries = ordered_entries.select_related("user", "race")
    
    all_races = Race.objects.all()
    context = {
        'top_entries': ordered_entries[:10],
        'all_races': all_races,
        'selected_race': race_title,
        'entry_count': ordered_entries.count()
    }
    
    return render(request, 'leaderboard/race_leaderboard.html', context)
