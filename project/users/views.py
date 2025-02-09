from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import Profile


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
