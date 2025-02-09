from django.urls import path, include
from . import views
from .views import home, register, sign_in, welcome, increment_points
urlpatterns = [   
    path('', home, name='home'),
    path('login/', views.sign_in, name='login'),
    path('register/', register, name='register'),
    path('welcome/', welcome, name='welcome'),
    path('tasks/', include('tasks.urls')),
    path('increment-points/', increment_points, name='increment_points'),
    ]
