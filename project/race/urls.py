from django.urls import path
from . import views

urlpatterns = [
    path('', views.race_view, name='race'),
    path('update-race-time/', views.update_race_time, name='update_race_time'),
    path('calculate-distance/', views.calculate_distance, name='calculate_distance'),
    path('create-race/', views.create_race, name='create_race'),
    path('update-race-time/', views.update_race_time, name='update_race_time')
]