from django.db.models import F, ExpressionWrapper, DurationField, CharField, IntegerField 
from django.db.models.functions import Round, Cast


def get_labeler_for_field(field_name):
    """Return the appropriate labeler function for the given field"""
    labelers = {
        'medal': add_label_medal,
        'duration': add_label_duration
    }
    return labelers.get(field_name)

def add_label_medal(race_queryset):
    # races already have a medal property
    return race_queryset

def add_label_duration(race_queryset):
    return race_queryset.annotate(
        duration=Cast(
            Round(
                ExpressionWrapper(F('end_time') - F('start_time'), output_field=DurationField()) / 1000000,
                0
            ),
            output_field=IntegerField()
        )
    )
