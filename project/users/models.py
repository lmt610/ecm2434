from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model() 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    other_field = models.CharField(max_length=100, default='default value')  
    points = models.IntegerField(default=0)
    exeplore_mode_distance_traveled = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'user_profile'):
        instance.user_profile.save()

class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location_tracking = models.BooleanField(default=True)
    show_on_leaderboard = models.BooleanField(default=True)
    route_notifications = models.BooleanField(default=True)
    achievement_notifications = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username}'s settings"

@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(
              user=instance,
              location_tracking=True,
              show_on_leaderboard=True,
              route_notifications=True,
              achievement_notifications=True
          )

