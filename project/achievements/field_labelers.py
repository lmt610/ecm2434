from django.db.models import Count, Avg, F, ExpressionWrapper, fields, Case, When, Value, IntegerField

def get_labeler_for_field(field_name):
    """Return the appropriate labeler function for the given field"""
    labelers = {
        'medal': add_label_medal,
    }
    return labelers.get(field_name)

def add_label_medal(race_queryset):
    # races already have a medal property
    return race_queryset
