import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Race, Location, RaceEntry
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import Profile
from math import radians, sin, cos, sqrt, atan2

@login_required
def race_view(request, race_id=None):
    if race_id is None:
        races = Race.objects.all()
        raceEntries=RaceEntry.objects.filter(user=request.user)
        return render(request,"race/race-menu.html", {"races": races, "raceEntries": raceEntries})
    else:
        race = get_object_or_404(Race, id=race_id)
        entry = RaceEntry.objects.filter(race=race, user=request.user).first()
        if(entry):
            duration = entry.get_duration()
            return render(request, "race/race.html", {"race": race, "entry": entry, "duration" : duration})
        else:
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
   

#adds time to the created race object IF the new time is smaller than the existing one for that object
@login_required
@csrf_exempt
def update_race_time(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

    data = json.loads(request.body)
    raceID = data.get("race_id")
    race = Race.objects.filter(id=raceID).first()
    if race == None:
         return JsonResponse({"status": "error", "message": "Race not found"}, status=404)

    start_time = parse_datetime(data.get("start_time"))
    end_time = parse_datetime(data.get("end_time"))
    entry, created = RaceEntry.objects.get_or_create(race=race, user=request.user)
    if created:
        entry.start_time = start_time
        entry.end_time = end_time
    else:
        #compare time to previous best
        current_pb = entry.get_duration()
        new_time = (end_time - start_time).total_seconds()
        if new_time < current_pb:
            entry.start_time = start_time
            entry.end_time = end_time
        entry.num_completions += 1
    
    entry.save()
    return JsonResponse({"status": "success", "message": "RaceEntry updated"})

def add_exeplore_points(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        try:
            user = Profile.objects.get(user__username=data.get("user"))
        except Profile.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"}, status=404)
        
        start_lat = data.get("start_latitude")
        start_lon = data.get("start_longitude")
        end_lat = data.get("end_latitude")
        end_lon = data.get("end_longitude")

        #distance is calculated in kilometres, multiply by 100 to get points in the 10s + 20 to add base points
        distance = haversine(start_lat, start_lon, end_lat, end_lon)
        points_to_add = 100 * distance + 20
        points_to_add = int(points_to_add)

        user.points += points_to_add
        user.exeplore_mode_distance_traveled += distance
        user.save()

        return JsonResponse({"points": points_to_add})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


