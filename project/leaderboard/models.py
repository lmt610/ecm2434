from django.db import models
from race.models import Race, RaceEntry
from django.contrib.auth.models import User

class LeaderboardEntry(models.Model):
    """Stores race results for the leaderboard"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    completion_time = models.FloatField(help_text="Time in seconds")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.race.title} - {self.completion_time}s"
