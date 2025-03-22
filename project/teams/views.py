from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Team, TeamJoinRequest
from .forms import TeamForm

@login_required
def team_list(request):
    teams = Team.objects.all()
    # Check if the user is admin of any teams
    user_is_admin = Team.objects.filter(admin=request.user).exists()
    
    context = {
        'teams': teams,
        'user_is_admin': user_is_admin
    }
    return render(request, 'teams/team_list.html', context)

@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    has_joined = team.members.filter(id=request.user.id).exists()
    join_request_pending = TeamJoinRequest.objects.filter(team=team, user=request.user, status='pending').exists()
    is_team_admin = (request.user == team.admin)

    return render(request, 'teams/team_detail.html', {
        'team': team, 
        'has_joined': has_joined, 
        'join_request_pending': join_request_pending,
        'is_team_admin': is_team_admin
    })
    
@login_required
def create_team(request):
    """Only admin users should be able to create teams"""
    if request.method == 'POST':
        form = TeamForm(request.POST)
        
        if form.is_valid():
            team = form.save(commit=False)
            team.admin = request.user
            team.save()
            # Add the creator as a member too
            team.members.add(request.user)
            messages.success(request, f"Team '{team.name}' created successfully!")
            return redirect('team_detail', pk=team.pk)
    else:
        form = TeamForm()
    
    return render(request, 'teams/create_team.html', {'form': form})

def request_join_team(request, pk):
    team = get_object_or_404(Team, pk=pk)

    # checks if already a member 
    if team.members.filter(id=request.user.id).exists():
        messages.error(request, "You are a member of this team.")
        return redirect('team_detail', pk=pk)
    
    # checks if request already submitted
    if TeamJoinRequest.objects.filter(team=team, user=request.user, status='pending').exists():
         messages.info(request, "You have requested to join this team.")
         return redirect('team_detail', pk=pk)

    # creates join request
    TeamJoinRequest.objects.create(team=team, user=request.user)
    messages.success(request, "Your request to join this team has been submitted.")
    return redirect('team_detail', pk=pk)

@login_required
def team_join_requests(request, pk):
    # Only team admin can view requests
    team = get_object_or_404(Team, pk=pk, admin=request.user)
    join_requests = TeamJoinRequest.objects.filter(team=team, status='pending')
    return render(request, 'teams/team_join_requests.html', {'team': team, 'join_requests': join_requests})

def approve_join_request(request, pk, request_id):
    team = get_object_or_404(Team, pk=pk, admin=request.user)
    join_request = get_object_or_404(TeamJoinRequest, pk=request_id, team=team, status='pending')

    if request.method == 'POST':
        join_request.status = 'approved'
        join_request.save()
        team.members.add(join_request.user)
        messages.success(request, f"{join_request.user.username} has been added to the team.")
        return redirect('team_join_requests', pk=pk)

    return render(request, 'teams/approve_join_request.html', {'team': team, 'join_request': join_request})

@login_required
def approve_join_request(request, pk, request_id):
    team = get_object_or_404(Team, pk=pk)
    
    # Check if user is admin
    if request.user != team.admin:
        return HttpResponseForbidden("You don't have permission to perform this action.")
        
    join_request = get_object_or_404(TeamJoinRequest, pk=request_id, team=team, status='pending')

    if request.method == 'POST':
        join_request.status = 'approved'
        join_request.save()
        team.members.add(join_request.user)
        messages.success(request, f"{join_request.user.username} has been added to the team.")
        return redirect('team_join_requests', pk=pk)

    return render(request, 'teams/approve_join_request.html', {'team': team, 'join_request': join_request})

@login_required
def reject_join_request(request, pk, request_id):
    team = get_object_or_404(Team, pk=pk)
    
    # Check if user is admin
    if request.user != team.admin:
        return HttpResponseForbidden("You don't have permission to perform this action.")
        
    join_request = get_object_or_404(TeamJoinRequest, pk=request_id, team=team, status='pending')

    if request.method == 'POST':
        join_request.status = 'rejected'
        join_request.save()
        messages.success(request, f"Join request from {join_request.user.username} has been rejected.")
        return redirect('team_join_requests', pk=pk)

    return render(request, 'teams/reject_join_request.html', {'team': team, 'join_request': join_request})


@login_required
def manage_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    
    # Only team admin can manage the team
    if request.user != team.admin:
        messages.error(request, "You don't have permission to manage this team.")
        return redirect('team_detail', pk=pk)
        
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, "Team updated successfully!")
            return redirect('team_detail', pk=pk)
    else:
        form = TeamForm(instance=team)
        
    return render(request, 'teams/manage_team.html', {'form': form, 'team': team})

@login_required
def remove_team_member(request, team_pk, user_pk):
    team = get_object_or_404(Team, pk=team_pk)
    
    # Check if current user is the team admin
    if request.user != team.admin:
        messages.error(request, "You don't have permission to remove members.")
        return redirect('team_detail', pk=team_pk)
        
    user_to_remove = get_object_or_404(User, pk=user_pk)
    
    # Cannot remove the admin
    if user_to_remove == team.admin:
        messages.error(request, "You cannot remove the team admin.")
        return redirect('team_detail', pk=team_pk)
        
    if request.method == 'POST':
        team.members.remove(user_to_remove)
        messages.success(request, f"{user_to_remove.username} has been removed from the team.")
        
    return redirect('team_detail', pk=team_pk)

def is_superuser(user):
    return user.is_superuser
