from django.urls import path
from . import views

urlpatterns = [
    path('', views.race_view, name='race'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),    
    path('leaderboard/', views.leaderboard_view, name='leaderboard_view'), 

]
