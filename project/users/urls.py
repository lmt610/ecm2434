from django.urls import path, include
from . import views
from .views import home, register, sign_in, log_out, welcome, increment_points, settings_view, delete_account, change_password, toggle_setting, update_email
urlpatterns = [   
    path('', home, name='home'),
    path('login/', sign_in, name='login'),
    path('register/', register, name='register'),
    path('logout/', log_out, name="log_out"),
    path('welcome/', welcome, name='welcome'),
    path('tasks/', include('tasks.urls')),
    path('teams/', include('teams.urls')),
    path('increment-points/', increment_points, name='increment_points'),
    path('settings/', settings_view, name='settings'),
    path('change-password/', change_password, name='change_password'),
    path('delete-account/', delete_account, name='delete_account'),
    path('toggle-setting/', toggle_setting, name='toggle_setting'),
    path('update-email/', update_email, name='update_email')
    ]
