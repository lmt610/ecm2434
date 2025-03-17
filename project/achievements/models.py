from django.db import models
from django.contrib.auth.models import User
from race.models import RaceEntry
from teams.models import Team
from django.core.exceptions import ValidationError
from .field_labelers import get_labeler_for_field

class Achievement(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    
    MODEL_CHOICES = [
        ('COUNT_RACES', 'Count Races'),
        ('COUNT_TEAMS', 'Count Teams'),
    ]
    
    OPERATOR_CHOICES = [
        ('<', 'Less than'),
        ('=', 'Equal to'),
        ('>', 'Greater than'),
    ]
    
    main_condition_model = models.CharField(max_length=20, choices=MODEL_CHOICES)
    main_condition_operator = models.CharField(max_length=2, choices=OPERATOR_CHOICES)
    main_condition_value = models.CharField(max_length=50)
    
    # Store subconditions as JSON array of [field, operator, value]
    subconditions = models.JSONField(default=list)
    
    # Static mapping of all allowed fields that can be used for achievements
    # make sure a labeler is added for each subcondition field
    MODEL_FIELDS = {
        'COUNT_RACES': [
            'medal',
            'duration',
            'distance',
            'position'
        ],
        'COUNT_TEAMS': [
            'number_of_members'
        ]
    }
    
    def __str__(self):
        return str(self.title)
    
    def clean(self):
        """Validate that subcondition fields match the main condition model"""
        super().clean()
        
        # Ensure subconditions is a list
        if not isinstance(self.subconditions, list):
            raise ValidationError("Subconditions must be a list")
        
        valid_fields = self.MODEL_FIELDS.get(str(self.main_condition_model),[])
        valid_operators = [op[0] for op in self.OPERATOR_CHOICES]
        
        for subcondition in self.subconditions:
            # subcondition must be of the format [field, operator, value]
            if not isinstance(subcondition, list) or len(subcondition) != 3:
                raise ValidationError("Each subcondition must be a list of [field, operator, value]")
            
            field, operator, value = subcondition
            
            if field not in valid_fields:
                raise ValidationError(
                    f"'{field}' is not a valid field for model '{self.main_condition_model}'"
                )
            
            if operator not in valid_operators:
                raise ValidationError(f"'{operator}' is not a valid operator")
            
            if not isinstance(value, str):
                raise ValidationError("Values must be strings")
    
    def has_user_completed(self, user):
        if self.main_condition_model == 'COUNT_RACES':
            base_query = RaceEntry.objects.filter(user=user)
        elif self.main_condition_model == 'COUNT_TEAMS':
            base_query = Team.objects.filter(members=user)
        else:
            return False
        
        # Apply all subconditions
        for subcondition in self.subconditions:
            field, operator, value = subcondition
           

            # Get the appropriate labeler function and apply it
            labeler = get_labeler_for_field(field)
            if labeler:
                # Apply the custom field labeler
                base_query = labeler(base_query)
                # Build dynamic query based on operator
                if operator == '<':
                    query_kwargs = {f"{field}__lt": value}
                elif operator == '=':
                    query_kwargs = {f"{field}": value}
                elif operator == '>':
                    query_kwargs = {f"{field}__gt": value}
                
                base_query = base_query.filter(**query_kwargs)

        # check whether main condition has been met
        count = base_query.count()
        if self.main_condition_operator == '<':
            return count < int(self.main_condition_value)
        elif self.main_condition_operator == '=':
            return count == int(self.main_condition_value)
        elif self.main_condition_operator == '>':
            return count > int(self.main_condition_value)
            
        return False
