from django.db.models.signals import post_save
from django.dispatch import receiver
from race.models import RaceEntry
from tasks.models import Task, UserTaskCompletion
from users.models import Profile

@receiver(post_save, sender=RaceEntry)
def check_task_completion(sender, instance, created, **kwargs):
    if created:
        tasks = Task.objects.all()
        for task in tasks:
            if not task.is_active():
                continue
            if task.task_type == 'multi':
                if (int(task.completed_races_count(instance.user)) >= int(task.required_races)):
                    if not UserTaskCompletion.objects.filter(user=instance.user, task=task).exists():
                        profile = Profile.objects.get(user=instance.user)
                        profile.points += task.points_awarded
                        profile.save()
                        # prevents the user from regaining points for completing the same task
                        UserTaskCompletion.objects.create(user=instance.user, task=task)
            elif task.task_type == 'single':
                if task.is_completed_by_user(instance.user):
                    if not UserTaskCompletion.objects.filter(user=instance.user, task=task).exists():
                        profile = Profile.objects.get(user=instance.user)
                        profile.points += task.points_awarded
                        profile.save()
                        UserTaskCompletion.objects.create(user=instance.user, task=task)
                    
