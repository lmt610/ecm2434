from django import forms
from .models import Team
from django.core.validators import MinLengthValidator, RegexValidator

class TeamForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3, 'Team name must be at least 3 characters long'),
            RegexValidator(
                regex=r'^[A-Za-z0-9\s\-_]+$',
                message='Team name can only contain letters, numbers, spaces, hyphens, and underscores',
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Enter team name'})
    )
    
    class Meta:
        model = Team
        fields = ['name']

class JoinTeamForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), label="Select Team")