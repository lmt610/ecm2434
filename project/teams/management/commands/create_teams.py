from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from teams.models import Team
import random

User = get_user_model()

class Command(BaseCommand):
    help = "Creates teams and users"

    def handle(self, *args, **kwargs):
        team_data = [
            {"name": "Mathematics"},
            {"name": "Computer Science"},
            {"name": "Philosophy"},
            {"name": "Classics"},
        ]

        user_data = [
            {"username": "user1", "password": "password1"},
            {"username": "user2", "password": "password2"},
            {"username": "user3", "password": "password3"},
            {"username": "user4", "password": "password4"},
            {"username": "user5", "password": "password5"},
        ]

        users = []
        superuser = User.objects.create_superuser(username='superuser', password='password')
        self.stdout.write(self.style.SUCCESS(f"Superuser '{superuser.username}' created."))

        for i in user_data:
            user, created = User.objects.get_or_create(username=i['username'])
            if created:
                user.set_password(i['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"User '{user.username}' created."))
            else:
                self.stdout.write(self.style.WARNING(f"User '{user.username}' already exists."))
            users.append(user)

        users.append(superuser)

        for i in team_data:
            admin_user = superuser
            team, created = Team.objects.get_or_create(name=i['name'], admin=admin_user)
            if created:
                team.points = random.randint(0, 100)
                team.save()
                self.stdout.write(self.style.SUCCESS(f"Team '{team.name}' created with {team.points} points."))
            else:
                self.stdout.write(self.style.WARNING(f"Team '{team.name}' already exists."))

            num_members = random.randint(1, len(users))  
            members = random.sample(users, num_members)  
            team.members.set(members)  
            team.save()
            members_usernames = [member.username for member in members]
            self.stdout.write(self.style.SUCCESS(f"Users {', '.join(members_usernames)} added to team '{team.name}'."))

        self.stdout.write(self.style.SUCCESS("Teams and users created successfully!"))
