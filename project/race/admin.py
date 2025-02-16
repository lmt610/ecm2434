from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import LeaderboardEntry
from .models import Race  # Import the Race model

admin.site.register(Race)  # Register the Race model

admin.site.register(LeaderboardEntry)
