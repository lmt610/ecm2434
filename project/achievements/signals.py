from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from .models import Achievement
from django.conf import settings

@receiver(post_migrate)
def populate_database_with_achievements(sender, **kwargs):
    """Populates the database with example achievements."""
    
    # Ensure this only runs for the 'achievements' app
    if sender.name != "achievements":
        return
   
    # skip these if testing
    if settings.TESTING:
        return

    ############
    ## RACE
    ############
    Achievement.objects.create(
            title="A Whole New World",
            description="Run a Race",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
            subconditions=[]
        )   
    Achievement.objects.create(
            title="Golden Beginnings",
            description="Get a gold medal",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
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
            description="Complete 5 races with a distance over 0.5km",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="4",
            subconditions=[
                ["distance", ">", "0.5"]
            ]
        )
    Achievement.objects.create(
            title="Are We There Yet?",
            description="Complete a race longer than 1km",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
            subconditions=[
                ["distance", ">", "1.0"]
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
    Achievement.objects.create(
            title="Deja Vu",
            description="Complete the same route 5 times",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
            subconditions=[
                ["number_of_completions", ">", "4"]
            ]
        )
    
    Achievement.objects.create(
            title="Can't Stop, Won't Stop",
            description="Complete the same route 10 times",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
            subconditions=[
                ["number_of_completions", ">", "19"]
            ]
        )

    Achievement.objects.create(
            title="Tour Guide",
            description="Complete the same route 50 times",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
            subconditions=[
                ["number_of_completions", ">", "49"]
            ]
        )
    
    Achievement.objects.create(
        title="Peak Performance",
        description="Get a gold medal on an uphill race",
        main_condition_model="COUNT_RACES",
        main_condition_operator=">",
        main_condition_value="0",
        subconditions=[
            ["tags", "contains", "uphill"],
            ["medal", "=", "gold"]
        ]
    )

    Achievement.objects.create(
        title="Summit to be Proud Of",
        description="Complete 5 uphill races",
        main_condition_model="COUNT_RACES",
        main_condition_operator=">",
        main_condition_value="4",
        subconditions=[
            ["tags", "contains", "uphill"],
        ]
    )

    ############
    ## TEAM
    ############
    Achievement.objects.create(
        title="Branching Out",
        description="Join a team",
        main_condition_model="COUNT_TEAMS",
        main_condition_operator=">",
        main_condition_value="0",
        subconditions=[]
    )
    Achievement.objects.create(
        title="Leafy Legion",
        description="Be part of a team with 20 members",
        main_condition_model="COUNT_TEAMS",
        main_condition_operator=">",
        main_condition_value="0",
        subconditions=[
            ["number_of_members", ">", "19"]
        ]
    )

    Achievement.objects.create(
        title="Playing the Field",
        description="Be a member of 5 teams",
        main_condition_model="COUNT_TEAMS",
        main_condition_operator=">",
        main_condition_value="4",
        subconditions=[]
    )

    print("Default achievements added")

