from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile
from teams.models import Team

User = get_user_model()

@receiver(post_migrate)
def populate_database(sender, **kwargs):
    """Populates essential data into the database after migrations."""
    
    # Ensure this only runs for the 'users' app
    if sender.name != "users":
        return
    
    # Create a default user if it doesn't exist
    # Check if the profile exists based on the username
    user_a = User.objects.filter(username="UserA").first()
    if user_a is None:
        user_a = User.objects.create_user(username="UserA", password="Password")
    
    user_b = User.objects.filter(username="UserB").first()
    if user_b is None:
        user_b = User.objects.create_user(username="UserB", password="Password")
    

    print("database populated with test users")

@receiver (post_save, sender=Profile)
def update_team_points(sender, instance, **kwargs):
    for team in instance.user.teams.all():
        team.update_points()