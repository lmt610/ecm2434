from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse
from .models import Team
from .forms import TeamForm
from django.shortcuts import render, redirect

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin')  
    actions = ['create_team_action']  

    def create_team_action(self, request, queryset):
        if request.method == 'POST':
            form = TeamForm(request.POST)
            if form.is_valid():
                team = form.save(commit=False)
                team.admin = request.user  
                team.save()
                self.message_user(request, "Team created successfully.", level=messages.SUCCESS)  
                return redirect(reverse('admin:teams_team_changelist'))  

            else:
                return render(request, 'admin/teams/create_team.html', {'form': form, 'team_admin': self})

        else:
            form = TeamForm()
            return render(request, 'admin/teams/create_team.html', {'form': form, 'team_admin': self})
        
    create_team_action.short_description = "Create New Team" 
