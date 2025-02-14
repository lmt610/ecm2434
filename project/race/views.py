import json
from django.shortcuts import render, get_object_or_404
from .models import Race, Location
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from math import radians, sin, cos, sqrt, atan2

def race_view(request,race_id):
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
            return JsonResponse({"status": "outside range", "distance": round(distance, 2)})
        
    return JsonResponse({"error": "Invalid request"}, status = 400)
