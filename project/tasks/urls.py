from django.urls import path
from .views import tasks, add_task_score  

urlpatterns = [
    path('tasks/', tasks, name='tasks'),
    path('add_score/<int:task_id>/', add_task_score, name='add_task_score'),
]
