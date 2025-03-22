from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from race.models import Race, RaceEntry, Location
from tasks.models import Task, UserTaskCompletion
from users.models import Profile
from tasks.signals import check_task_completion
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

User = get_user_model()

class TaskSignalTests(TestCase):
    def setUp(self):
        # creates user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # ensures profile only gets created once
        self.profile, created = Profile.objects.get_or_create(user=self.user, defaults={'points': 0})

        self.location = Location.objects.create(
            name='Test Location1',
            latitude=33.30,
            longitude=36.18,
        )

        self.start_date = timezone.now()
        self.end_date = self.start_date + timezone.timedelta(days=1)

        # creates race
        self.start_time = timezone.now()
        self.end_time = self.start_time + timezone.timedelta(days=1)  # sets end time a day later
        self.race = Race.objects.create(
            title='Test Race',
            start=self.location,
            end=self.location,
        )

        # creates tasks
        self.single_task = Task.objects.create(
            title='Single Task',
            race=self.race,
            points_awarded=20,
            required_races=1,
            task_type='single',
            start_date = self.start_date,
            end_date = self.end_date,
        )
        self.multi_task = Task.objects.create(
            title='Multi Task',
            race=None,
            points_awarded=20,
            required_races=2,
            task_type='multi',
            start_date = self.start_date,
            end_date = self.end_date,
        )

    def reset_profile_points(self):
        """sets profile points to zero."""
        self.profile.refresh_from_db()
        self.profile.points = 0
        self.profile.save()

    def test_single_task_completion(self):
        self.reset_profile_points()

        # user completes race for single task
        RaceEntry.objects.create(user=self.user, race=self.race,)

        self.assertTrue(UserTaskCompletion.objects.filter(user=self.user, task=self.single_task).exists())
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.points, 20)

    def test_multi_task_completion_exact(self):
        self.reset_profile_points()

        # user completes multi and single task
        RaceEntry.objects.create(user=self.user, race=self.race,)
        RaceEntry.objects.create(user=self.user, race=self.race,)

        self.assertTrue(UserTaskCompletion.objects.filter(user=self.user, task=self.multi_task).exists())
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.points, 40)

    def test_no_duplicate_task_completion(self):
        self.reset_profile_points()

        RaceEntry.objects.create(user=self.user, race=self.race,)

        # first completion
        self.assertTrue(UserTaskCompletion.objects.filter(user=self.user, task=self.single_task).exists())

        # user completes the race again
        RaceEntry.objects.create(user=self.user, race=self.race,)

        race_entry = RaceEntry.objects.last()

        RaceEntry.objects.create(user=self.user, race=self.race,)

        race_entry = RaceEntry.objects.last()

        # check only one completion exists
        self.assertEqual(UserTaskCompletion.objects.filter(user=self.user, task=self.single_task).count(), 1)
        self.assertEqual(UserTaskCompletion.objects.filter(user=self.user, task=self.multi_task).count(), 1)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.points, 40)

    def test_empty_task_list(self):
        self.reset_profile_points()

        # clears all tasks
        Task.objects.all().delete()

        # user completes a race
        RaceEntry.objects.create(user=self.user, race=self.race,)

        # no tasks should trigger any completion
        self.assertEqual(UserTaskCompletion.objects.count(), 0)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.points, 0)

    def test_multiple_users_completion(self):
        other_user = User.objects.create_user(username='another_user', password='password')
        Profile.objects.get_or_create(user=other_user, defaults={'points': 0})

        # user 1 completes the race
        RaceEntry.objects.create(user=self.user, race=self.race,)

        # user 2 completes the race
        RaceEntry.objects.create(user=other_user, race=self.race,)
        RaceEntry.objects.create(user=other_user, race=self.race,)

        # check if both users are awarded points correctly
        self.assertTrue(UserTaskCompletion.objects.filter(user=self.user, task=self.single_task).exists())
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.points, 20)

        self.assertTrue(UserTaskCompletion.objects.filter(user=other_user, task=self.single_task).exists())
        other_user_profile = Profile.objects.get(user=other_user)
        other_user_profile.refresh_from_db()
        self.assertEqual(other_user_profile.points, 40)

    def test_race_completed_task_not_complete_until_task_assigned(self):
        self.reset_profile_points()

        RaceEntry.objects.create(user=self.user, race=self.race,)

        self.assertTrue(RaceEntry.objects.filter(user=self.user, race=self.race,).exists())

        delayed_single_task = Task.objects.create(
            title='Delayed Single Task',
            race=self.race,
            points_awarded=20,
            required_races=1,
            task_type='single'
        )

        race_entry = RaceEntry.objects.last()

        # assert that the task is not completed
        self.assertFalse(UserTaskCompletion.objects.filter(user=self.user, task=delayed_single_task).exists())

        UserTaskCompletion.objects.create(user=self.user, task=delayed_single_task)

        self.assertTrue(UserTaskCompletion.objects.filter(user=self.user, task=delayed_single_task).exists())
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.points, 20)
