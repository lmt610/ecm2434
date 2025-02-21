from django.contrib import admin
from .models import Race, Location

class RaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end', 'start_time', 'end_time', 'is_complete')
    list_filter = ('is_complete', 'start_time')
    search_fields = ('title')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    search_fields = ('name',)

admin.site.register(Race, RaceAdmin)
admin.site.register(Location, LocationAdmin)

