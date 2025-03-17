from users.models import Profile
from django.shortcuts import render, redirect
from tasks.models import Task
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def tasks(request):
    user_tasks = []
    tasks = Task.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())

    for task in tasks:
        if task.task_type == 'single':
            is_completed = task.is_completed_by_user(request.user)
            user_tasks.append({
                'task': task,
                'is_completed': is_completed,
                'count': None,
                'progress_percentage': 100 if is_completed else 0
            })
        elif task.task_type == 'multi':
            completed_count = task.completed_races_count(request.user)

            if completed_count > task.required_races:
                completed_count = task.required_races

            progress_percentage = (completed_count / task.required_races * 100)
            user_tasks.append({
                'task': task,
                'is_completed': completed_count >= task.required_races,
                'count': completed_count,
                'progress_percentage': progress_percentage
            })

    return render(request, 'tasks/tasks.html', {'user_tasks': user_tasks})

