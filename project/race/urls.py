from django.urls import path
from . import views

urlpatterns = [
    path('', views.race_view, name='race'),
    path('<int:race_id>/', views.race_view, name='race_detail'),
    path('update-race-time/', views.update_race_time, name='update_race_time'),
    path('calculate-distance/', views.calculate_distance, name='calculate_distance'),
    # path('create-race/', views.create_race, name='create_race'),
    path('update-race-time/', views.update_race_time, name='update_race_time'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard_view'),    
    path('race/leaderboard/', views.leaderboard, name='raceleaderboard'), 
]
