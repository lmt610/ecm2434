from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371 #radius of earth in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def validate_ascending_three_items(value):
    if not isinstance(value, list):
        raise ValidationError("This field must be a list")

    if len(value) != 3:
        raise ValidationError("This field must contain exactly 3 items")
    
    for elem in value:
        if not isinstance(elem, int):
            raise ValidationError("Elements in this field must be integers")


    if value[0] > value[1] or value[1] > value[2]:
        raise ValidationError("Values in this field must be in ascending order")

def validate_list_of_strings(value):
    if not isinstance(value, list):
        raise ValidationError("Field Value must be a list.")
    
    if not all(isinstance(item, str) for item in value):
        raise ValidationError("All items in the list must be strings.")

class Race(models.Model):
    title = models.CharField(max_length=255)
    start = models.ForeignKey('Location', related_name='start_races', on_delete=models.CASCADE)
    end = models.ForeignKey('Location', related_name='end_races', on_delete=models.CASCADE)
    medal_requirements = models.JSONField(default=list, validators=[validate_ascending_three_items])
    tags = models.JSONField(default=list, validators=[validate_list_of_strings])    

    def __str__(self):
        return str(self.title)
    
    def get_distance(self):
        return haversine(self.start.latitude,self.start.longitude,self.end.latitude,self.end.longitude)
        

class RaceEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField(default=None, null=True, blank=True)
    end_time = models.DateTimeField(default=None, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    medal = models.CharField(max_length=6, default='None')
    num_completions=models.IntegerField(default=0)
    rank = models.IntegerField(null=True, blank=True) 

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"{self.race} {self.user}"

        if self.start_time is not None and self.end_time is not None:
            self.assign_medal()  

        super().save(*args, **kwargs)

    def get_duration(self):
        if (self.end_time == None or self.start_time == None):
            return None
        return (self.end_time - self.start_time).total_seconds()

    def get_duration_in_minutes(self):
        duration = self.get_duration()
        return duration / 60

    def assign_medal(self):
        """Assigns a medal based on race completion time."""
        medals = ["Gold", "Silver", "Bronze"]

        for i in range(len(self.race.medal_requirements)):
            if self.get_duration() <= self.race.medal_requirements[i]:
                self.medal = medals[i]
                break
        else:
            self.medal = "None"

    def assign_ranks():
        race_entries = RaceEntry.objects.all().order_by('duration')  # Sort by race duration
        for i, entry in enumerate(race_entries):
            entry.rank = i + 1  # 1st place gets rank 1, 2nd place gets rank 2, etc.
            entry.save()


    @classmethod
    def get_num_completed_races(cls,user):
        return cls.objects.filter(user=user).count()
    
    @classmethod
    def get_total_distance_travled_by_user(cls,user):
        entrys = cls.objects.filter(user=user)
        user_distance = 0
        for entry in entrys:
            times_completed = entry.num_completions
            race_length = entry.race.get_distance()
            user_distance = user_distance + (race_length*times_completed)
        return user_distance

    @property
    def race_date(self):
        return self.start_time.date()

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
