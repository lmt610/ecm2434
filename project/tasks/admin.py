from django.contrib import admin
from .models import Task, UserTaskCompletion

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'race', 'points_awarded', 'required_races', 'task_type', 'start_date', 'end_date', 'created_at')
    search_fields = ('title',)
    list_filter = ('race', 'task_type',)
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
      
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'points_awarded', 'start_date', 'end_date', 'task_type')
	    }),
        ('Single-Race Task (leave blank for tasks of type multiple)', {
            'fields': ('race',)
	    }),
        ('Multi-Race Task (leave blank for tasks of type single)', {
 	        'fields': ('required_races',)
	    }),
     )
  
admin.site.register(Task, TaskAdmin)
admin.site.register(UserTaskCompletion)
