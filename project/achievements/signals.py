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
    Achievement.objects.get_or_create(
            title="A Whole New World",
            description="Run a race",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
            subconditions=[]
        )
    Achievement.objects.get_or_create(
            title="Rising Star",
            description="Run 10 races",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="9",
            subconditions=[]
        )
    Achievement.objects.get_or_create(
            title="Seasoned Veteran",
            description="Run 100 races",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="99",
            subconditions=[]
        )
    Achievement.objects.get_or_create(
            title="Bronze Beginnings",
            description="Get a bronze medal",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
            subconditions=[
                ["medal", "=", "bronze"]
            ]
    )
    Achievement.objects.get_or_create(
            title="Silvery Success",
            description="Get a silver medal",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
            subconditions=[
                ["medal", "=", "silver"]
            ]
    )
    Achievement.objects.get_or_create(
            title="Golden Glory",
            description="Get a gold medal",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
            subconditions=[
                ["medal", "=", "gold"]
            ]
        )
    Achievement.objects.get_or_create(
            title="Sprinter",
            description="Complete 2 races in under 1 minute",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="1",
            subconditions=[
                ["duration", "<", "60"]
            ]
        )
    Achievement.objects.get_or_create(
            title="The Long Game",
            description="Complete 10 races with a distance over 0.5km",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="9",
            subconditions=[
                ["distance", ">", "0.5"]
            ]
        )
    Achievement.objects.get_or_create(
            title="Are We There Yet?",
            description="Complete a race longer than 1km",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
            subconditions=[
                ["distance", ">", "1.0"]
            ]
        )
    Achievement.objects.get_or_create(
            title="Marathon Master",
            description="Complete 10 races longer than 1km",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="9",
            subconditions=[
                ["distance", ">", "1.0"]
            ]
        )
    Achievement.objects.get_or_create(
            title="Double Crown",
            description="Hold the top leaderboard position on two races",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="1",
            subconditions=[
                ["position", "=", "1"]
            ]
        )
    Achievement.objects.get_or_create(
            title="Deja Vu",
            description="Complete the same route 5 times",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
            subconditions=[
                ["number_of_completions", ">", "4"]
            ]
        )
    Achievement.objects.get_or_create(
            title="Can't Stop, Won't Stop",
            description="Complete the same route 10 times",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
            subconditions=[
                ["number_of_completions", ">", "19"]
            ]
        )
    Achievement.objects.get_or_create(
            title="Tour Guide",
            description="Complete the same route 50 times",
            main_condition_model="COUNT_RACES",
            main_condition_operator=">",
            main_condition_value="0",
            subconditions=[
                ["number_of_completions", ">", "49"]
            ]
        )
    Achievement.objects.get_or_create(
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
    Achievement.objects.get_or_create(
        title="Summit to be Proud Of",
        description="Complete 5 uphill races",
        main_condition_model="COUNT_RACES",
        main_condition_operator=">",
        main_condition_value="4",
        subconditions=[
            ["tags", "contains", "uphill"],
        ]
    )
    Achievement.objects.get_or_create(
        title="Summit Special",
        description="Complete 10 uphill races",
        main_condition_model="COUNT_RACES",
        main_condition_operator=">",
        main_condition_value="9",
        subconditions=[
            ["tags", "contains", "uphill"],
        ]
    )
    Achievement.objects.get_or_create(
        title="Break a Leg",
        description="Complete 100 uphill races",
        main_condition_model="COUNT_RACES",
        main_condition_operator=">",
        main_condition_value="99",
        subconditions=[
            ["tags", "contains", "uphill"],
        ]
    )
    ############
    ## TEAM
    ############
    Achievement.objects.get_or_create(
        title="Branching Out",
        description="Join a team",
        main_condition_model="COUNT_TEAMS",
        main_condition_operator=">",
        main_condition_value="0",
        subconditions=[]
    )
    Achievement.objects.get_or_create(
        title="Leafy Legion",
        description="Be part of a team with 20 members",
        main_condition_model="COUNT_TEAMS",
        main_condition_operator=">",
        main_condition_value="0",
        subconditions=[
            ["number_of_members", ">", "19"]
        ]
    )
    Achievement.objects.get_or_create(
        title="Playing the Field",
        description="Be a member of 5 teams",
        main_condition_model="COUNT_TEAMS",
        main_condition_operator=">",
        main_condition_value="4",
        subconditions=[]
    )

    print("Default achievements added")

