from django.urls import path
from . import views

urlpatterns = [
    path('join/', views.request_join_team, name='join_team'),
    path('list/', views.team_list, name='team_list'),
    path('', views.team_list, name='team_list'),
    path('create/', views.create_team, name='create_team'),
    path('<int:pk>/', views.team_detail, name='team_detail'),
    path('<int:pk>/request_join/', views.request_join_team, name='request_join_team'),
    path('<int:pk>/join_requests/', views.team_join_requests, name='team_join_requests'),
    path('<int:pk>/approve_join_request/<int:request_id>/', views.approve_join_request, name='approve_join_request'),
    path('<int:pk>/reject_join_request/<int:request_id>/', views.reject_join_request, name='reject_join_request'),
    path('<int:pk>/manage/', views.manage_team, name='manage_team'),
    path('<int:team_pk>/remove_team_member/<int:user_pk>/', views.remove_team_member, name='remove_team_member'),
]