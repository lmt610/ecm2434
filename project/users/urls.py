from django.urls import path, include
from . import views
from .views import *

urlpatterns = [   
    path('', welcome, name='welcome'),
    path('login/', sign_in, name='login'),
    path('register/', register, name='register'),
    path('logout/', log_out, name="log_out"),
    path('dashboard/', dashboard, name='dashboard'),
    path('tasks/', include('tasks.urls')),
    path('teams/', include('teams.urls')),
    path('increment-points/', increment_points, name='increment_points'),
    path('settings/', settings_view, name='settings'),
    path('change-password/', change_password, name='change_password'),
    path('delete-account/', delete_account, name='delete_account'),
    path('toggle-setting/', toggle_setting, name='toggle_setting'),
    path('update-email/', update_email, name='update_email')
    ]
