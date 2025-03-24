from django.db import models
from django.conf import settings
from race.models import validate_list_of_strings
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save
from users.models import Profile

class Team(models.Model):
    name = models.CharField(max_length=100)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='admin_of', on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams', blank=True)
    points = models.IntegerField(default=0)
    tags = models.JSONField(default=list, validators=[validate_list_of_strings])

    def __str__(self):
        return str(self.name)

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


@receiver(post_save, sender=Profile)
def recalculate_team_points(sender, instance, created, **kwargs):
    # Get all the teams the user belongs to
    user_teams = instance.user.teams.all()  # This gets all teams the user is a part of
    
    # Loop through each team the user belongs to
    for team in user_teams:
        # Recalculate the team's points based on the sum of points of all users in the team
        total_points = sum([profile.points for user in team.members.all() if hasattr(user, 'user_profile') for profile in [user.user_profile]])
        
        # Set the team points to the total of all members' points
        team.points = total_points
        team.save()  # Save the updated team points



@receiver(m2m_changed, sender=Team.members.through)
def recalculate_team_points_on_member_addition(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        for user_id in pk_set:
            user = model.objects.get(id=user_id)
            total_points = sum([profile.points for user in instance.members.all() if hasattr(user, 'user_profile') for profile in [user.user_profile]])
            instance.points = total_points
            instance.save()