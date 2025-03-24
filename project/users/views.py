from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm
from .models import Profile, UserSettings
from race.models import RaceEntry, Streak
from achievements.models import Achievement 
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from tasks.models import Task, UserTaskCompletion
from teams.models import Team
from django.db.models import Min, Q 
from django.utils import timezone


User = get_user_model()

def get_user_settings(request):
    return UserSettings.objects.get(user=request.user)

def welcome(request):
    return render(request, 'users/welcome.html')

def log_out(request):
    logout(request)
    return redirect('welcome')
    

def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('dashboard')

        form = LoginForm()
        return render(request,'users/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('dashboard')
        
        # form is not valid or user is not authenticated
        messages.error(request,f'Invalid username or password')
        return render(request,'users/login.html',{'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            # creates user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # hash password
            user.save()

            login(request, user)
            messages.success(request, 'Your account has been created!')
            return redirect('dashboard')  
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')

        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard(request):
        if request.user.is_authenticated:
            #define dynamic values to be passed to the template
            user = request.user
            user_profile = Profile.objects.get(user=request.user)
            users_total = len(Profile.objects.all())
            tasks_complete = UserTaskCompletion.get_num_completed_tasks(user_profile.user)
            races_complete = RaceEntry.get_num_completed_races(user_profile.user)
            streak_model = Streak.objects.filter(user=request.user).first()
            achievements_earned = len(Achievement.get_all_user_achievements(user_profile.user))
            achievements_total = len(Achievement.objects.all())
            teams_total = len(Team.objects.all())
            team_first_queryset  = Team.objects.all().order_by('-points')[:1]
            team_second_queryset = Team.objects.all().order_by('-points')[1:2]
            team_third_queryset = Team.objects.all().order_by('-points')[2:3]
            tasks_total = len(Task.objects.all())
            race_entries_total = len(RaceEntry.objects.filter(user=user))

            # extract the team names from the QuerySets
            team_first = team_first_queryset[0].name if team_first_queryset else None
            team_second = team_second_queryset[0].name if team_second_queryset else None
            team_third = team_third_queryset[0].name if team_third_queryset else None


            user = request.user
            race_entries = RaceEntry.objects.filter(user=user).exclude(Q(start_time=None) | Q(end_time=None))

            user = request.user
            race_entries = (
                RaceEntry.objects.filter(user=user)
                .annotate(duration=Min('end_time') - Min('start_time'))
                .filter(duration__gt=timezone.timedelta(seconds=0))  # ensures the duration is greater than 0
            )

            fastest_race_entry = race_entries.order_by('duration').first()

            fastest_race_name = None
            fastest_race_time = None

            if fastest_race_entry:
                fastest_race_name = fastest_race_entry.race.title  
                fastest_time = fastest_race_entry.end_time - fastest_race_entry.start_time
                fastest_race_time = round(fastest_time.total_seconds()) if fastest_time else None

            distance_covered = user_profile.exeplore_mode_distance_traveled + RaceEntry.get_total_distance_travled_by_user(user_profile.user)
            print(tasks_complete, races_complete)
            context = {
                'user_score': user_profile.points,
            }

            try:
                current_streak = streak_model.current_streak if streak_model else 0
                longest_streak = streak_model.longest_streak if streak_model else 0
            except Streak.DoesNotExist:
                current_streak = 0
                longest_streak = 0

            return render(request, 'users/dashboard.html', {
                'username': request.user.username,
                'user_score': user_profile.points,
                'users_total' : users_total,
                'tasks_completed' : tasks_complete,
                'races_completed' : races_complete,
                'achievements_earned' : achievements_earned,
                'achievements_total' : achievements_total,
                'teams_total' : teams_total,
                'team_first' : team_first,
                'team_second' : team_second,
                'team_third' : team_third, 
                'tasks_total' : tasks_total,
                'distance_covered' : distance_covered,
                'fastest_race_name': fastest_race_name,
                'fastest_race_time': fastest_race_time,
                'race_entries_total' : race_entries_total,
                'current_streak': current_streak,
                'longest_streak': longest_streak,
            })
        else:
            return redirect('login')

@login_required
def increment_points(request):
    if request.method == 'POST':
        try:
            points_change = int(request.POST.get('points', 0))
            profile = request.user.profile
            profile.points += points_change
            profile.save()
            response_data = {
                'success': True,
                'new_points': profile.points
            }
        except ValueError:
            response_data = {
                'success': False,
                'error': 'Invalid points.'
            }
        return JsonResponse(response_data)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def settings_view(request):
    context = {
        'user': request.user,
        'settings': get_user_settings(request),
    }
    return render(request, 'users/settings.html', context)

@login_required
def change_password(request): 
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return JsonResponse({
                'status': 'success',
                'message': 'Your password was successfully updated!'
            })
        else:
            # Convert form errors to simple dict with error messages
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = str(error_list[0])  # Convert to string and take first error
            return JsonResponse({
                'status': 'error',
                'errors': errors
            }, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('welcome')
    return redirect('settings')

@login_required
def update_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        if new_email:
            email_validator = EmailValidator()
            try:
                email_validator(new_email)
                request.user.email = new_email
                request.user.save()
                messages.success(request, 'Email updated successfully!')
            except ValidationError:
                messages.error(request, "Please provide a valid email")
        else:
            messages.error(request, 'Please provide a valid email.')
    return redirect('settings')

@login_required
def toggle_setting(request):
    if request.method == 'POST':
        setting_name = request.POST.get('setting')
        if setting_name==None or request.POST.get('value')==None:
            return JsonResponse({'status':'error'},status=400)

        value = request.POST.get('value') == 'true'
        
        user_settings = UserSettings.objects.get(user=request.user)
        if hasattr(user_settings, setting_name):
            setattr(user_settings, setting_name, value)
            user_settings.save()
            return JsonResponse({'status': 'success'})
            
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def export_user_data(request):
    user = request.user  # Get logged-in user
    user_settings = UserSettings.objects.filter(user=user).first()

    # Generate user data in JSON format
    user_data = {
        "user_data_export": {
            "username": user.username,
            "email": user.email,
            "settings_preferences": {
                "allow_location_tracking": user_settings.location_tracking,
                "show_user_activity_on_leaderboard": user_settings.show_on_leaderboard
            },
            "notes": [
                "If you would like to change these details, you can do so in the settings menu.",
                "If you would like this information to no longer be stored, you can delete your account from the settings menu."
            ]
        }
    }

    # Return a JSON response
    return JsonResponse(user_data, safe=False)
