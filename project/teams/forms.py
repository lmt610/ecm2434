from django import forms
from .models import Team

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']

class JoinTeamForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), label="Select Team")
