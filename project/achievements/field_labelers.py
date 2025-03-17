from django.db.models import F, ExpressionWrapper, DurationField, CharField, IntegerField, Func, FloatField 
from django.db.models.functions import Round, Cast, Radians, Sqrt, Cos, Power, Sin, ATan2
from django.db.models.expressions import RawSQL

def get_labeler_for_field(field_name):
    """
        Return the appropriate labeler function for the given field.
        This function should named add_label_{field_name}
    """
    labelers = {
        'medal': add_label_medal,
        'duration': add_label_duration,
        'distance': add_label_distance
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

def add_label_distance(race_queryset):
    """Uses the Haversine formula to annotate a query containing Race objects with their distance"""
    race_queryset = race_queryset.select_related('race__start', 'race__end')
    
    lat1 = Radians(F('race__start__latitude'))
    lon1 = Radians(F('race__start__longitude'))
    lat2 = Radians(F('race__end__latitude'))
    lon2 = Radians(F('race__end__longitude'))

    # use haversine formula to calculate distance
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = Power(Sin(dlat/2), 2) + Cos(lat1) * Cos(lat2) * Power(Sin(dlon/2), 2)
    c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
    R = 6371  # Earth radius in km
    distance = R * c
    
    distance_expr = ExpressionWrapper(distance, output_field=FloatField())
    return race_queryset.annotate(distance=distance_expr)
