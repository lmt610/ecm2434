from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from .models import Achievement

@receiver(post_migrate)
def populate_database_with_achievements(sender, **kwargs):
    """Populates the database with example achievements."""
    
    # Ensure this only runs for the 'achievements' app
    if sender.name != "achievements":
        return
    
    Achievement.objects.create(
            title="A Whole New World",
            description="Run a Race",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
            subconditions=[]
        )   

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
    Achievement.objects.create(
            title="Sprinter",
            description="Complete 2 races in under 1 minute",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="1",
            subconditions=[
                ["duration", "<", "60"]
            ]
        )
    Achievement.objects.create(
            title="The Long Game",
            description="Complete 2 races with a distance over 0.5km",
            main_condition_model="COUNT_RACES",
            main_condition_operator="=",
            main_condition_value="2",
            subconditions=[
                ["distance", ">", "0.5"]
            ]
        )
    Achievement.objects.create(
            title="Double Crown",
            description="Hold the top leaderboard position on two races",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="1",
            subconditions=[
                ["position", "=", "1"]
            ]
        )

    print("Example achievements added")

