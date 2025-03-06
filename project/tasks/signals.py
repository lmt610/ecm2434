from django.db.models.signals import post_save
from django.dispatch import receiver
from race.models import RaceEntry
from tasks.models import Task
from users.models import Profile

@receiver(post_save, sender=RaceEntry)
def check_task_completion(sender, instance, created, **kwargs):
    if created:
        tasks = Task.objects.all()
        for task in tasks:
            if task.task_type == 'multi':
                if (int(task.completed_races_count(instance.user)) >= int(task.required_races)) or (task.required_races == 0):
                      profile = Profile.objects.get(user=instance.user)
                      profile.points += task.points_awarded
                      profile.save()
                     
            elif task.task_type == 'single':
                if task.is_completed_by_user(instance.user):
                      profile = Profile.objects.get(user=instance.user)
                      profile.points += task.points_awarded
                      profile.save()
