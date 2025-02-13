from django.shortcuts import render, get_object_or_404
from .models import Race
def race_view(request,race_id):
    race = get_object_or_404(Race, id=race_id)
    return render(request,"race/race.html", {"race": race})
