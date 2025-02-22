from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

@receiver(post_migrate)
def populate_database(sender, **kwargs):
    """Populates essential data into the database after migrations."""
    
    # Ensure this only runs for the 'users' app
    if sender.name != "users":
        return
    
    # Create a default user if it doesn't exist
    if not User.objects.filter(username="UserA").exists():
        user = User.objects.create_user(username="UserA", password="Password")
        profile, created = Profile.objects.get_or_create(user=user, other_field="12345678", points=0)

    if not User.objects.filter(username="UserB").exists():
        user = User.objects.create_user(username="UserB", password="Password")
        profile, created = Profile.objects.get_or_create(user=user, other_field="12345678", points=0)