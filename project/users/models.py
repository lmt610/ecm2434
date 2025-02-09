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
