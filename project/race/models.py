from django.db import models

class Race(models.Model):
    title = models.CharField(max_length=255)
    start = models.ForeignKey('Location', related_name='start_races', on_delete=models.CASCADE)
    end = models.ForeignKey('Location', related_name='end_races', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_complete = models.BooleanField()

    def __str__(self):
        return self.title
    
    def get_duration(self):
        return self.end_time - self.start_time

    def get_duration_in_minutes(self):
        duration = self.get_duration()
        return duration.total_seconds() / 60
    
    @property
    def race_date(self):
        return self.start_time.date()  # This extracts the date part from the start_time

class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name