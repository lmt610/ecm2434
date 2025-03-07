from django.urls import path
from .views import tasks, add_task_score  

urlpatterns = [
    path('tasks/', tasks, name='tasks'),
]
