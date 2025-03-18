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

logger = logging.getLogger(__name__)
def race_leaderboard(request):
    try:
        # Get all races for the filter dropdown - log to verify we're getting races
        all_races = Race.objects.all()
        logger.info(f"Found {all_races.count()} races")
        
        # Get race title from query parameters
        race_title = request.GET.get("race_title")
        logger.info(f"Filtering by race title: {race_title}")
        
        # Get all race entries with related user and race data
        race_entries = RaceEntry.objects.select_related("user", "race").all()
        
        # Log initial count
        logger.info(f"Initial race entries count: {race_entries.count()}")
        
        # Filter race entries by race title if provided
        if race_title:
            race_entries = race_entries.filter(race__title__icontains=race_title)
            logger.info(f"After filtering by race title: {race_entries.count()} entries")
        
        # Filter out entries without start or end times
        valid_entries = []
        for entry in race_entries:
            if entry.start_time and entry.end_time:
                # Calculate the completion time in seconds
                try:
                    entry.completion_time = (entry.end_time - entry.start_time).total_seconds()
                    valid_entries.append(entry)
                except Exception as e:
                    logger.error(f"Error calculating completion time for entry {entry.id}: {e}")
        
        logger.info(f"Valid entries after filtering: {len(valid_entries)}")
        
        # Sort by completion time (fastest first)
        sorted_entries = sorted(valid_entries, key=lambda x: x.completion_time)
        
        # Get the top 10 entries
        top_entries = sorted_entries[:10]
        
        logger.info(f"Final top entries count: {len(top_entries)}")
        
        # Log some sample data for debugging
        if top_entries:
            sample = top_entries[0]
            logger.info(f"Sample entry - Race: {sample.race.title}, User: {sample.user.username}, Time: {sample.completion_time}")
        
        context = {
            'top_entries': top_entries,
            'all_races': all_races,
            'selected_race': race_title,
            'entry_count': len(valid_entries)
        }
        
        return render(request, 'leaderboard/race_leaderboard.html', context)
    
    except Exception as e:
        logger.error(f"Error in race_leaderboard view: {e}", exc_info=True)
        # Return a simple error view if something goes wrong
        context = {
            'error': str(e),
            'all_races': Race.objects.all(),
            'selected_race': race_title
        }
        return render(request, 'leaderboard/race_leaderboard.html', context)