from django.contrib import admin
from .models import Profile
# username: admin, password: password
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'other_field', 'points')
    search_fields = ('user__username', 'other_field')
    list_filter = ('user__is_active', 'user__is_staff')

admin.site.register(Profile, ProfileAdmin)
