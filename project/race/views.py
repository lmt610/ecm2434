import json, random
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Race, Location, RaceEntry, Streak
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.utils.timezone import localdate
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import Profile
from achievements.models import Achievement
from math import radians, sin, cos, sqrt, atan2
from users.views import UserSettings


@login_required
def race_view(request, race_id=None):
    if race_id is None:
        races = Race.objects.all()
        raceEntries=RaceEntry.objects.filter(user=request.user)
        return render(request,"race/race-menu.html", {"races": races, "raceEntries": raceEntries})
    else:
        race = get_object_or_404(Race, id=race_id)
        entry = RaceEntry.objects.filter(race=race, user=request.user).first()
        user_location_preferance = UserSettings.objects.filter(user=request.user).first().location_tracking
        if(entry):
            duration = entry.get_duration()
            return render(request, "race/race.html", {"race": race, "entry": entry, "duration" : duration, "location_tracking" : user_location_preferance})
        else:
            return render(request,"race/race.html", {"race": race, "location_tracking" : user_location_preferance})

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

    achievements_before_race = Achievement.get_all_user_achievements(request.user) 

    start_time = parse_datetime(data.get("start_time"))
    end_time = parse_datetime(data.get("end_time"))
    entry = RaceEntry.objects.filter(race=race, user=request.user).first() 
    if entry is None: 
        RaceEntry.objects.create(
            race=race,
            user=request.user,
            start_time=start_time,
            end_time=end_time
        )
    else:
        current_pb = entry.get_duration()
        new_time = (end_time - start_time).total_seconds()
        if new_time < current_pb:
            entry.start_time = start_time
            entry.end_time = end_time
        entry.num_completions += 1

    update_streak(request.user)    
    entry.save()
    
    nature_fact = get_random_nature_fact()
    achievements_after_race = Achievement.get_all_user_achievements(request.user)
    new_achievements = achievements_after_race.difference(achievements_before_race).values("title", "description")
    if(new_achievements.count()>0):
        return JsonResponse({
            "status": "success", 
            "message": "RaceEntry updated", 
            "new_achievements": list(new_achievements),
            "nature_fact": nature_fact
        })
    else:
         return JsonResponse({
             "status": "success", 
             "message": "RaceEntry updated",
             "nature_fact": nature_fact
         })


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

        #distance is calculated in kilometres, students earn 2 points for every 10 meters, and a baseline 30 pointsas a bias
        distance = haversine(start_lat, start_lon, end_lat, end_lon)
        points_to_add = 200 * distance + 30
        points_to_add = int(points_to_add)

        user.points += points_to_add
        user.exeplore_mode_distance_traveled += distance
        user.save()

        return JsonResponse({"points": points_to_add})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

def update_streak(user):
    streak, created = Streak.objects.get_or_create(user=user)

    if streak.date_of_last_race == localdate():
        return #race already completed
    
    if streak.date_of_last_race == localdate() - timedelta(days=1):
        streak.current_streak += 1 #continue the streak
    else:
        streak.current_streak = 1 #reset the streak

    streak.date_of_last_race = localdate()
    streak.save()

def get_random_nature_fact():
    """Return a random nature fact about University of Exeter campus."""
    nature_facts = [
        "The University of Exeter's campus is home to over 10,000 trees, making it one of the greenest university campuses in the UK!",
        "Reed Hall Gardens at the University of Exeter features exotic trees from around the world, including a giant sequoia!",
        "The University of Exeter's campus is home to several species of bats, including the rare greater horseshoe bat!",
        "The azaleas and rhododendrons that bloom on Exeter's campus in spring were originally planted in the 1860s!",
        "The University of Exeter's campus ponds support diverse wildlife, including three species of newts!",
        "Did you know? The University of Exeter has its own arboretum with over 300 tree species from across the globe!",
        "Exeter's campus is a haven for pollinators with special wildflower zones that support over 25 bee species!",
        "The hedgerows across Exeter's campus provide vital corridors for wildlife to move safely between habitats!",
        "Exeter's campus features multiple rain gardens that naturally filter rainwater and reduce flooding!",
        "Some of the oak trees on Exeter's campus are over 400 years old and predate the university itself!",
        "The University of Exeter's grounds team uses organic gardening practices across 95% of the campus!",
        "Exeter's campus meadows are managed specifically to support declining butterfly populations!",
        "The reed beds at Exeter's campus ponds naturally filter water while providing habitat for dragonflies!",
        "Campus gardeners at Exeter have installed over 200 nest boxes to support bird populations!",
        "The University of Exeter has several champion trees - specimens that are the largest of their species in Devon!"
    ]
    return random.choice(nature_facts)
