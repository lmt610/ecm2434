from django.contrib import admin
from .models import Race, Location, RaceEntry, Streak

class RaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end',)
    list_filter = ('start','end',)
    search_fields = ('title',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude',)
    search_fields = ('name',)

class RaceEntryAdmin(admin.ModelAdmin):
    list_display = ('race', 'user', 'name', 'start_time', 'end_time', 'medal')

admin.site.register(Race, RaceAdmin)
admin.site.register(RaceEntry, RaceEntryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Streak)
