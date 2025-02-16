from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import LoginForm, UserRegistrationForm
from .models import Profile, UserSettings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()

def home(request):
    return render(request, 'users/home.html')

def sign_in(request):
    if request.method == 'GET':
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
                return redirect('welcome')
        
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

            messages.success(request, 'Your account has been created!')
            return redirect('login')  

    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def welcome(request):
        if request.user.is_authenticated:
            user_profile = Profile.objects.get(user=request.user)

            context = {
                'user_score': user_profile.points,
                }
            return render(request, 'users/welcome.html', {
                'username': request.user.username,
                'user_score': user_profile.points  
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
    try:
        user_settings = UserSettings.objects.get(user=request.user)
    except UserSettings.DoesNotExist:
        user_settings = UserSettings.objects.create(
            user=request.user,
            location_tracking=True,
            show_on_leaderboard=True,
            route_notifications=True,
            achievement_notifications=True
        )
    
    context = {
        'user': request.user,
        'settings': user_settings,
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
        return redirect('home')
    return redirect('settings')

@login_required
def update_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        if new_email:
            request.user.email = new_email
            request.user.save()
            messages.success(request, 'Email updated successfully!')
        else:
            messages.error(request, 'Please provide a valid email.')
    return redirect('settings')

@login_required
def toggle_setting(request):
    if request.method == 'POST':
        setting_name = request.POST.get('setting')
        value = request.POST.get('value') == 'true'
        
        try:
            user_settings = UserSettings.objects.get(user=request.user)
            if hasattr(user_settings, setting_name):
                setattr(user_settings, setting_name, value)
                user_settings.save()
                return JsonResponse({'status': 'success'})
        except UserSettings.DoesNotExist:
            pass
            
    return JsonResponse({'status': 'error'}, status=400)