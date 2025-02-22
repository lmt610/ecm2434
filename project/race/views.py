import json
from django.http import JsonResponse
from .models import LeaderboardEntry
from django.shortcuts import render, get_object_or_404
from .models import Race, Location
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from math import radians, sin, cos, sqrt, atan2

@login_required
def race_view(request, race_id=None):
    if race_id is None:
        races = Race.objects.all()
        return render(request,"race/race-menu.html", {"races": races})
    else:
        race = get_object_or_404(Race, id=race_id)
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
        #check if distance is within threshold (e.g., 20m)
        threshold = 0.05
        print(distance)
        if distance <= threshold:
            return JsonResponse({"status": "within range", "distance": round(distance, 2)})
        else:
            return JsonResponse({"status": "outside range", "distance": round(distance, 2)})
        
    return JsonResponse({"error": "Invalid request"}, status = 400)

@csrf_exempt
#creates a race object when a user chooses two locations
def create_race(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title")
        start_id = data.get("start_id")
        end_id = data.get("end_id")

        #logic added to return an existing race to the frontend if the user enters a previously used start and end combination
        for race in Race.objects.all():
            if start_id == race.start.id and end_id == race.end.id:
                return JsonResponse({"status": "success", "message": "Race already registered with user", "race_id": race.id})

        try:
            start_location = Location.objects.get(id=start_id)
            end_location = Location.objects.get(id=end_id)
            race = Race.objects.create(
                title=title,
                start=start_location,
                end=end_location,
                start_time=None,
                end_time=None,
                is_complete=False
            )

            return JsonResponse({"status": "success", "race_id": race.id})
        except Location.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invalid locations"}, status=400)
        
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
    
@csrf_exempt
#adds time to the created race object IF the new time is smaller than the existing one for that object
def update_race_time(request):
    if request.method == "POST":
        data = json.loads(request.body)
        race_id = data.get("race_id")
        print(race_id)
        print(data.get("start_time"),data.get("end_time"))
        start_time = parse_datetime(data.get("start_time"))
        end_time = parse_datetime(data.get("end_time"))
        try:
            race = Race.objects.get(id=race_id)

            if race.start_time is None or race.end_time is None:
                #if start_time or end_time is null, set them
                race.start_time = start_time
                race.end_time = end_time
            else:
                #compare times
                current_pb = race.get_duration().total_seconds()
                new_time = (end_time - start_time).total_seconds()
                print(current_pb, new_time)
                if new_time < current_pb:
                    race.start_time = start_time
                    race.end_time = end_time
            print("setting completion to true")
            race.is_complete = True
            race.save()

            return JsonResponse({"status": "success", "message": "Race updated"})
        except Race.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Race not found"}, status=404)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
    
def leaderboard(request):
    """Returns the leaderboard for a specific race, sorted by completion time"""
    race_id = request.GET.get("race_id")  # Get race ID from the frontend
    
    if race_id:
        leaderboard_entries = LeaderboardEntry.objects.filter(race_id=race_id).order_by("completion_time")[:10]
    else:
        leaderboard_entries = LeaderboardEntry.objects.order_by("completion_time")[:10]  # Default top 10 (all races)

    data = [
        {
            "user": entry.user.username,
            "race": entry.race.title,
            "time": entry.completion_time,
            "date": entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for entry in leaderboard_entries
    ]
    return JsonResponse({"leaderboard": data})

def leaderboard_view(request):
    race_title = request.GET.get("race_title")
    if race_title:
                # race title search is case insensitive
        leaderboard_entries = LeaderboardEntry.objects.filter(race__title__icontains=race_title).order_by('completion_time').select_related('user', 'race')
    else:
        leaderboard_entries = LeaderboardEntry.objects.order_by('completion_time').select_related('user', 'race')
        
    top_entries = leaderboard_entries[:10]
    entries_count = leaderboard_entries.count()

    context = {
        'top_entries': top_entries,
    }
    return render(request, 'race/leaderboard.html', context)