from django.db import models
from django.contrib.auth.models import User

class Race(models.Model):
    title = models.CharField(max_length=255)
    start = models.ForeignKey('Location', related_name='start_races', on_delete=models.CASCADE)
    end = models.ForeignKey('Location', related_name='end_races', on_delete=models.CASCADE)
    medal_requirements = models.JSONField(default=list)
    

    def __str__(self):
        return self.title

class RaceEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='RaceEntry')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    is_complete = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    medal = models.CharField(max_length=6, default='None')


    def save(self, *args, **kwargs):
        if self.start_time != None and self.end_time!=None:
            self.duration = self.end_time - self.start_time
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def get_duration(self):
        return self.end_time - self.start_time

    def get_duration_in_minutes(self):
        duration = self.get_duration()
        return duration.total_seconds() / 60
    
    @property
    def race_date(self):
        return self.start_time.date()  # This extracts the date part from the start_time
    
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
        
class LeaderboardEntry(models.Model):
    """Stores race results for the leaderboard"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    completion_time = models.FloatField(help_text="Time in seconds")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.race.title} - {self.completion_time}s"
