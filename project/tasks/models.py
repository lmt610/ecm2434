from django.db import models
from django.contrib.auth import get_user_model
from race.models import Race, RaceEntry
from django.utils import timezone

User = get_user_model()

class Task(models.Model):
    TASK_TYPE_CHOICES = (
        ('single', 'Single Race Task'),
        ('multi', 'Multiple Race Task'),
    )

    title = models.CharField(max_length=255)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, null=True, blank=True)
    points_awarded = models.IntegerField(default=20)
    required_races = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    task_type = models.CharField(max_length=10, choices=TASK_TYPE_CHOICES, default='multi')

    def __str__(self):
        return self.title

    def is_completed_by_user(self, user):
        if self.task_type == 'single':
            return RaceEntry.objects.filter(
                user=user,
                race=self.race,
                is_complete=True,
                timestamp__gte=self.created_at
                ).exists()
        elif self.task_type == 'multi':
            # TODO completed races function
            return False

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date


