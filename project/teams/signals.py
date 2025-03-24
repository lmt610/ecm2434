from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from teams.models import Team

@receiver(m2m_changed, sender=Team.members.through)
def update_team_points(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        instance.update_points()