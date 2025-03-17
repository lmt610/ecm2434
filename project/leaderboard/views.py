from django.shortcuts import render
from users.models import Profile, UserSettings
from teams.models import Team
from race.models import RaceEntry
from django.db.models import F, ExpressionWrapper, DurationField


def user_leaderboard(request):
    # Fetch all profiles ordered by points
    ranked_profiles = Profile.objects.all().order_by('-points')

    # Don't show users on the leaderboard if their "Show my activities on leaderboards" setting off
    leaderboard_prefereance_settings = UserSettings.objects.filter(show_on_leaderboard=False)
    users_not_to_be_shown = [user_setting.user for user_setting in leaderboard_prefereance_settings]
    ranked_profiles = ranked_profiles.exclude(user__in=users_not_to_be_shown)

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
    
    # remove entries of users with their "Show my activities on leaderboards" setting off
    leaderboard_prefereance_settings = UserSettings.objects.filter(show_on_leaderboard=False)
    users_not_to_be_shown = [user_setting.user for user_setting in leaderboard_prefereance_settings]
    ordered_entries = ordered_entries.exclude(user__in=users_not_to_be_shown)


    top_entries = ordered_entries.select_related("user", "race")[:10]

    return render(request, 'leaderboard/race_leaderboard.html', {'top_entries':top_entries})


