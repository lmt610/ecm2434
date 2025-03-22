from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone
from .models import Location, Race

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
    #if not Race.objects.filter(title="Armory (A) to Streatham Court (CQ)").exists():
    #    Race.objects.create(
    #        title="Armory (A) to Streatham Court (CQ)",
    #        start=loc2,
    #        end=loc3,
    #    )
    #if not Race.objects.filter(title="Forum (North) to Physics Entrance").exists():    
    #    Race.objects.create(
    #        title="Forum (North) to Physics Entrance",
    #        start=loc1,
    #        end=loc4,
    #    ),
    #if not Race.objects.filter(title="Physics Entrance to Armory (A)").exists(): 
    #    Race.objects.create(
    #        title="Physics Entrance to Armory (A)",
    #        start=loc4,
    #        end=loc2,
    #    )
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
