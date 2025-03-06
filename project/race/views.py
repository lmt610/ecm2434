import json
from django.http import JsonResponse
from .models import LeaderboardEntry
from django.shortcuts import render, get_object_or_404
from .models import Race, Location, RaceEntry
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from math import radians, sin, cos, sqrt, atan2

@login_required
def race_view(request, race_id=None):
    if race_id is None:
        races = Race.objects.all()
        raceEntries=RaceEntry.objects.filter(user=request.user)
        return render(request,"race/race-menu.html", {"races": races, "raceEntries": raceEntries})
    else:
        race = get_object_or_404(Race, id=race_id)
        try:
            entry = get_object_or_404(RaceEntry, race=race, user=request.user)
            return render(request,"race/race.html", {"race": race, "entry": entry})
        except:
            pass
        return render(request,"race/race.html", {"race": race})

#haversine formula to calculate distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371 #radius of earth in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

@csrf_exempt #change later to properly account for Cross Site Request Forgery
def calculate_distance(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_lat, user_lon = float(data["latitude"]), float(data["longitude"])
        place_lat, place_lon = float(data["targetLatitude"]), float(data["targetLongitude"])
        #calculate distance using Haversine
        distance = haversine(user_lat, user_lon, place_lat, place_lon)
        #check if distance is within threshold (e.g., 50m)
        threshold = 0.05
        if distance <= threshold:
            return JsonResponse({"status": "within range", "distance": round(distance, 2)})
        else:
            return JsonResponse({"status": "outside range", "distance": round(distance, 2)})
        
    return JsonResponse({"error": "Invalid request"}, status = 400)
   
@csrf_exempt
#adds time to the created race object IF the new time is smaller than the existing one for that object
def update_race_time(request):
    if request.method == "POST":
        data = json.loads(request.body)
        raceID = data.get("race_id")
        try:
            race = Race.objects.get(id=raceID)
        except Race.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Race not found"}, status=404)
        try:
          user = User.objects.get(username=data.get("user"))
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"}, status=404)
        
        start_time = parse_datetime(data.get("start_time"))
        end_time = parse_datetime(data.get("end_time"))
        
        entry, _ = RaceEntry.objects.get_or_create(
            race=race,
            user=user,
            defaults={
                "name": f"{race} {user}",
                "user": user,
                "race": race,
                "start_time": None,
                "end_time": None,
                "is_complete": False
            })

        if entry.start_time is None or entry.end_time is None:
            entry.start_time = start_time
            entry.end_time = end_time
        else:
            #compare time to previous best
            current_pb = entry.get_duration()
            new_time = (end_time - start_time).total_seconds()
            if new_time < current_pb:
                entry.start_time = start_time
                entry.end_time = end_time
        entry.is_complete = True
        entry.save()

        return JsonResponse({"status": "success", "message": "RaceEntry updated"})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
    
def leaderboard(request):
    """Returns the leaderboard for a specific race, sorted by completion time"""
    race_id = request.GET.get("race_id")  # Get race ID from the frontend
    
    if race_id:
        leaderboard_entries = RaceEntry.objects.filter(race_id=race_id).order_by("duration")[:10]
    else:
        leaderboard_entries = RaceEntry.objects.order_by("duration")[:10]  # Default top 10 (all races)

    data = [
        {
            "user": entry.user.username,
            "race": entry.race.title,
            "time": entry.duration,
            "date": entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for entry in leaderboard_entries
    ]
    return JsonResponse({"leaderboard": data})

def leaderboard_view(request):
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
    return render(request, 'race/leaderboard.html', context)
