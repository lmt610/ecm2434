from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Achievement

@login_required
def achievements_view(request):
    all_achievements = Achievement.objects.all()
    
    user_achievements = Achievement.get_all_user_achievements(request.user)
    
    achievements_data = []
    
    for achievement in all_achievements:
        is_completed = achievement in user_achievements
        
        if achievement.main_condition_model == 'COUNT_RACES':
            category = 'race'
        elif achievement.main_condition_model == 'COUNT_TEAMS':
            category = 'team'
        else:
            category = 'other'
        
        achievements_data.append({
            'title': achievement.title,
            'description': achievement.description,
            'completed': is_completed,
            'category': category
        })
    
    return render(request, 'achievements/achievements.html', {
        'achievements': achievements_data
    })
