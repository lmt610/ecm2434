from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Achievement

@receiver(post_migrate)
def populate_database(sender, **kwargs):
    """Populates essential data into the database after migrations."""
    
    # Ensure this only runs for the 'race' app
    if sender.name != "achievements":
        return

    Achievement.objects.create(
        title="Gold Collector",
        description="Get a gold medal on 5 races",
        main_condition_model="COUNT_RACES",
        main_condition_operator="<",
        main_condition_value="4",
        subconditions=[
            ["medal", "=", "gold"]
        ]
    )
