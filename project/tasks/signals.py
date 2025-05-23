from django.db.models.signals import post_save
from django.dispatch import receiver
from race.models import RaceEntry
from tasks.models import Task, UserTaskCompletion
from users.models import Profile
from teams.models import Team

@receiver(post_save, sender=RaceEntry)
def check_task_completion(sender, instance, created, **kwargs):
    tasks = Task.objects.all()
    for task in tasks:
        if not task.is_active():
            continue
            
        # check if the race entry's start time is after the task's creation time
        if instance.updated_at and instance.updated_at >= task.start_date:
            if task.task_type == 'multi':
                completed_count = task.completed_races_count(instance.user)
                if completed_count >= task.required_races:
                    if not UserTaskCompletion.objects.filter(user=instance.user, task=task).exists():
                        profile = Profile.objects.get(user=instance.user)
                        profile.points += task.points_awarded
                        for team in Team.objects.filter(members=instance.user):
                            team.points += task.points_awarded
                            team.save()
                        profile.save()
                        UserTaskCompletion.objects.create(user=instance.user, task=task)
            elif task.task_type == 'single':
                if task.is_completed_by_user(instance.user):
                    if not UserTaskCompletion.objects.filter(user=instance.user, task=task).exists():
                        profile = Profile.objects.get(user=instance.user)
                        profile.points += task.points_awarded
                        for team in Team.objects.filter(members=instance.user):
                            team.points += task.points_awarded
                            team.save()
                        profile.save()
                        UserTaskCompletion.objects.create(user=instance.user, task=task)
