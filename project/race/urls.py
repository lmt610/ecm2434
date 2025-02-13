from django.urls import path
from . import views


urlpatterns = [
    path('', views.race_view, name='race'),
    path('<int:race_id>/', views.race_view, name='race_detail'),
]