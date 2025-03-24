from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Location, Race, RaceEntry 
from users.models import Profile  
from django.db.models import F, ExpressionWrapper, DurationField, Min


@receiver(post_migrate)
def populate_database(sender, **kwargs):
    """Populates essential data into the database after migrations."""
    
    # Ensure this only runs for the 'race' app
    if sender.name != "race":
        return

    # Create default locations if they don't exist
    loc1, created1 = Location.objects.get_or_create(name="Forum (North)", latitude=50.735836, longitude=-3.533852)
    loc2, created2 = Location.objects.get_or_create(name="Armory (A)", latitude=50.736859, longitude=-3.531877)
    loc3, created3 = Location.objects.get_or_create(name="Streatham Court (CQ)", latitude=50.735710, longitude=-3.530659)
    loc4, created4 = Location.objects.get_or_create(name="Physics Entrance", latitude=50.736766, longitude=-3.536608)
    sports_park_loc, _ = Location.objects.get_or_create(name="Sports Park Entrance", latitude=50.737498, longitude=-3.537124)
    community_gardens_loc, _ = Location.objects.get_or_create(name="Community Gardens", latitude=50.740448, longitude=-3.529612)
    arab_studies_loc, _ = Location.objects.get_or_create(name="Institute of Arab & Islamic Studies", latitude=50.736319, longitude=-3.536716)
    reed_pond_loc, _ = Location.objects.get_or_create(name="Reed Pond", latitude=50.733950, longitude=-3.537296)
    lemon_grove_loc, _ = Location.objects.get_or_create(name="Lemon Grove", latitude=50.735097, longitude=-3.530182)
    east_park_brook_loc, _ = Location.objects.get_or_create(name="East Park Brook", latitude=50.737770, longitude=-3.525151)
    locX, adminTest = Location.objects.get_or_create(name="St John's road (Test)", latitude=50.729075, longitude=-3.512862)
    locY, adminTest = Location.objects.get_or_create(name="Innovation centre (Test)", latitude=50.738326, longitude=-3.531160)

    # Create a default races if none exist
    if not Race.objects.filter(title="Forum (North) to Armory (A)").exists():
        Race.objects.create(
            title="Forum (North) to Armory (A)",
            start=loc1,
            end=loc2,
            medal_requirements=[150, 180, 300],
        )

    if not Race.objects.filter(title="Sports Park to Community Gardens").exists(): 
        Race.objects.create(
            title="Sports Park to Community Gardens",
            start=sports_park_loc,
            end=community_gardens_loc,
            medal_requirements=[150, 180, 300],
        )
    if not Race.objects.filter(title="Reed Pond to Arab & Islamic Studies").exists(): 
        Race.objects.create(
            title="Reed Pond to Arab & Islamic Studies",
            start=reed_pond_loc,
            end=arab_studies_loc,
            tags="uphill"
        )
    if not Race.objects.filter(title="Lemon Grove to East Park Brook").exists(): 
        Race.objects.create(
            title="Lemon Grove to East Park Brook",
            start=lemon_grove_loc,
            end=east_park_brook_loc,
            medal_requirements=[150, 180, 300],
            tags="uphill"
        )
    if  not Race.objects.filter(title="St John's road (Test)").exists(): 
        Race.objects.create(
            title="St John's road (Test)",
            start=locX,
            end=locX,
            medal_requirements=[5, 10, 15],
        )

    if not Race.objects.filter(title="Innovation centre (Test)").exists(): 
        Race.objects.create(
            title="Innovation centre (Test)",
            start=locY,
            end=locY,
            medal_requirements=[5, 10, 15],
        )
        print("Database populated with initial race data")




@receiver(post_save, sender=RaceEntry)
def award_medal_points(sender, instance, created, **kwargs):
    """Awards points to the user when a medal is assigned."""
    if created:  # Only process newly created RaceEntry objects
        medal_points = {"Gold": 30, "Silver": 20, "Bronze": 10}
        ranking_points = {1: 20, 2: 15, 3: 10}

        profile = Profile.objects.get(user=instance.user)

        # Award medal points
        if instance.medal in medal_points:
            profile.points += medal_points[instance.medal]
        else:
            profile.points += 5  # Default points for participation

        # Calculate the ranking **based on each user's best time**
        duration = ExpressionWrapper(F('end_time') - F('start_time'), output_field=DurationField())

        # Get the best (fastest) entry per user
        best_entries = (
            RaceEntry.objects
            .filter(race=instance.race)
            .values("user_id")
            .annotate(best_time=Min(duration))
        )

        # Convert to a sorted list of times
        sorted_times = sorted([entry["best_time"] for entry in best_entries])

        # Find where the current user's new entry ranks
        user_time = instance.end_time - instance.start_time
        user_rank = sorted_times.index(user_time) + 1 if user_time in sorted_times else None

        # Award ranking points if applicable
        if user_rank and user_rank in ranking_points:
            profile.points += ranking_points[user_rank]

        profile.save()  # Save the updated profile