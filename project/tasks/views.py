from users.models import Profile
from django.shortcuts import render, redirect

def tasks(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user, points=0)

    context = {
        'user_score': user_profile.points,
    }
    return render(request, 'tasks/tasks.html', context)
    return render(request, 'user/welcome.html', context) 

def add_task_score(request, task_id):  
    user_profile = Profile.objects.get(user=request.user)
    
    # placeholder for now
    task_points = {
        1: 10,
        2: 20,
        3: 30,
    }

    points = task_points.get(task_id, 0)

    user_profile.points += points
    user_profile.save()

    return redirect('tasks')
