from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Team, TeamJoinRequest
from django.contrib import messages

def team_list(request):
    teams = Team.objects.all()
    return render(request, 'teams/team_list.html', {'teams': teams})

def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    has_joined = team.members.filter(id=request.user.id).exists()
    join_request_pending = TeamJoinRequest.objects.filter(team=team, user=request.user, status='pending').exists()

    return render(request, 'teams/team_detail.html', {'team': team, 'has_joined': has_joined, 'join_request_pending':join_request_pending})

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

def team_join_requests(request, pk):
    team = get_object_or_404(Team, pk=pk, admin=request.user) # only team admin can view this
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

def reject_join_request(request, pk, request_id):
    team = get_object_or_404(Team, pk=pk, admin=request.user)
    join_request = get_object_or_404(TeamJoinRequest, pk=request_id, team=team, status='pending')

    if request.method == 'POST':
        join_request.status = 'rejected'
        join_request.save()
        messages.success(request, f"Join request from {join_request.user.username} has been rejected.")
        return redirect('team_join_requests', pk=pk)

    return render(request, 'teams/reject_join_request.html', {'team': team, 'join_request': join_request})

def is_superuser(user):
    return user.is_superuser
