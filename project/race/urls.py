from django.urls import path
from . import views

urlpatterns = [
    path('', views.race_view, name='race'),
]