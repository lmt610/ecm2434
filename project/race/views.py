from django.shortcuts import render

def race_view(request):
    return render(request,"race/templates/race.html")
