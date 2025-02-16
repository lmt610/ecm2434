from django.urls import path
from . import views
from .views import create_team, request_join_team, team_list

urlpatterns = [
    path('create/', create_team, name='create_team'),
    path('join/', request_join_team, name='join_team'),
    path('list/', team_list, name='team_list'),
    path('', views.team_list, name='team_list'),
    path('<int:pk>/', views.team_detail, name='team_detail'),
    path('<int:pk>/request_join/', views.request_join_team, name='request_join_team'),
    path('<int:pk>/join_requests/', views.team_join_requests, name='team_join_requests'),
    path('<int:pk>/approve_join_request/<int:request_id>/', views.approve_join_request, name='approve_join_request'),
    path('<int:pk>/reject_join_request/<int:request_id>/', views.reject_join_request, name='reject_join_request'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
