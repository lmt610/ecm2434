from django.db import models
from django.contrib.auth import get_user_model
from race.models import Race, RaceEntry
from django.utils import timezone
from django.core.validators import MinValueValidator

User = get_user_model()

class Task(models.Model):
    TASK_TYPE_CHOICES = (
        ('single', 'Single Race Task'),
        ('multi', 'Multiple Race Task'),
    )

    title = models.CharField(max_length=255)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, null=True, blank=True)
    points_awarded = models.IntegerField(default=20)
    required_races = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    task_type = models.CharField(max_length=10, choices=TASK_TYPE_CHOICES, default='single')

    def __str__(self):
        return self.title

    def completed_races_count(self, user):
        if self.race:
            count = RaceEntry.objects.filter(
                user=user,
                race=self.race,
                start_time__isnull=False,
                updated_at__gte=self.created_at  
            ).count()
            return count
        else:
            count = RaceEntry.objects.filter(
                user=user,
                start_time__isnull=False,
                updated_at__gte=self.created_at 
            ).count()
            return count

    def is_completed_by_user(self, user):
        if self.task_type == 'single':
            return RaceEntry.objects.filter(
                user=user,
                start_time__isnull=False,
                race=self.race,
                updated_at__gte=self.created_at 
            ).exists()
        elif self.task_type == 'multi':
            return self.completed_races_count(user) >= self.required_races

    def is_active(self):
        now = timezone.now()
        if self.start_date is None or self.end_date is None:
            return False  # task is inactive if dates are not set
        return self.start_date <= now <= self.end_date

class UserTaskCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_num_completed_tasks(cls,user):
        return cls.objects.filter(user=user).count()
    
    class Meta:
        unique_together = ('user', 'task')


