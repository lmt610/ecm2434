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

    # 🏁 Create default locations if they don't exist
    loc1, created1 = Location.objects.get_or_create(name="Forum (North)", latitude=50.735836, longitude=-3.533852)
    loc2, created2 = Location.objects.get_or_create(name="Armory (A)", latitude=50.736859, longitude=-3.531877)
    loc3, created3 = Location.objects.get_or_create(name="Streatham Court (CQ)", latitude=50.735710, longitude=-3.530659)
    loc4, created4 = Location.objects.get_or_create(name="Physics Entrance", latitude=50.736766, longitude=-3.536608)
    locX, adminTest = Location.objects.get_or_create(name="St Jhons road", latitude=50.729075, longitude=-3.512862)

    # 🏎️ Create a default races if none exist
    if not Race.objects.filter(title="Forum (North) to Armory (A)").exists():
        Race.objects.create(
            title="Forum (North) to Armory (A)",
            start=loc1,
            end=loc2,
        )
    if not Race.objects.filter(title="Armory (A) to Streatham Court (CQ)").exists():
        Race.objects.create(
            title="Armory (A) to Streatham Court (CQ)",
            start=loc2,
            end=loc3,
        )
    if not Race.objects.filter(title="Forum (North) to Physics Entrance").exists():    
        Race.objects.create(
            title="Forum (North) to Physics Entrance",
            start=loc1,
            end=loc4,
        ),
    if not Race.objects.filter(title="Physics Entrance to Armory (A)").exists(): 
        Race.objects.create(
            title="Physics Entrance to Armory (A)",
            start=loc4,
            end=loc2,
        )
    if not Race.objects.filter(title="St Jhons road").exists(): 
        Race.objects.create(
            title="St Jhons road",
            start=locX,
            end=locX,
        )

        print("✅ Database populated with initial race data!")
