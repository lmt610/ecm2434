import json
from .models import Location
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from math import radians, sin, cos, sqrt, atan2

def race_view(request):
    return render(request,"race/race.html")

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

        #Example of getting a stored location in the db
        place = Location.objects.first() #change to fetch the correct place
        place_lat, place_lon = place.latitude, place.longitude

        #calculate distance using Haversine
        distance = haversine(user_lat, user_lon, place_lat, place_lon)

        #check if distance is within threshold (e.g., 20m)
        threshold = 0.02
        if distance <= threshold:
            return JsonResponse({"status": "within range", "distance": round(distance, 2)})
        else:
            return JsonResponse({"status": "within range", "distance": round(distance, 2)})
        
    return JsonResponse({"error": "Invalid request"}, status = 400)



from django.http import JsonResponse
from .models import LeaderboardEntry
from collections import defaultdict

def leaderboard(request):
    """Returns the leaderboard grouped by race and sorted by completion time"""
    
    # Fetch all leaderboard entries, sorted by race first, then by completion time
    leaderboard_entries = LeaderboardEntry.objects.order_by("race", "completion_time")

    # Group results by race
    race_leaderboard = defaultdict(list)

    for entry in leaderboard_entries:
        race_leaderboard[entry.race.title].append({
            "user": entry.user.username,
            "time": entry.completion_time,
            "date": entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return JsonResponse({"leaderboard": dict(race_leaderboard)})
