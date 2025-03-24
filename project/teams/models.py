from django.db import models
from django.conf import settings
from race.models import validate_list_of_strings
from users.models import Profile 

class Team(models.Model):
    name = models.CharField(max_length=100)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='admin_of', on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams', blank=True)
    points = models.IntegerField(default=0)
    tags = models.JSONField(default=list, validators=[validate_list_of_strings])

    def __str__(self):
        return str(self.name)
    
    def update_points(self):
        total_points = Profile.objects.filter(user_in=self.members.all()).aggregate(models.Sum('points'))['points_sum']
        self.points = total_points if total_points else 0
        self.save()

class TeamJoinRequest(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ), default='pending')

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Join request for {self.user.username} to {self.team.name}'

