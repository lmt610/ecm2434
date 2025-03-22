import json
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now, timedelta
from race.models import Race, User, RaceEntry, Location
from users.models import Profile
from django.contrib.auth.models import User


class RaceMenuPageTests(TestCase):
    def setUp(self):
        # Create test Race objects 
        loc1 = Location.objects.create(name="Forum (North)", latitude=50.735836, longitude=-3.533852)
        loc2 = Location.objects.create(name="Armory (A)", latitude=50.736859, longitude=-3.531877)
        self.race1 = Race.objects.create(title="Race 1", start=loc1, end=loc2)
        self.race2 = Race.objects.create(title="Race 2", start=loc1, end=loc2)
        # User needed for authorised get request 
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_race_menu_contains_correct_number_of_maps(self):

        self.client.login(username='testuser', password='password')

        response = self.client.get(reverse("race"))  

        self.assertEqual(response.status_code, 200)

        # Count occurrences of the map div in the rendered response
        num_maps_in_html = response.content.decode().count('class="map"')

        # Ensure the count matches the number of Race entries
        self.assertEqual(num_maps_in_html, Race.objects.count())


class CalculateDistanceViewTests(TestCase):

    def setUp(self):
        self.url = reverse("calculate_distance")

    def test_calculate_distance_within_range(self):
        #Test when the user is within the 50m threshold
        data = {
            "latitude": 40.712776,
            "longitude": -74.005974,
            "targetLatitude": 40.712780,
            "targetLongitude": -74.005970
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "within range")

    def test_calculate_distance_outside_range(self):
        #Test when the user is outside the 50m threshold
        data = {
            "latitude": 40.712776,
            "longitude": -74.005974,
            "targetLatitude": -40.713800,  
            "targetLongitude": 74.006900
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "outside range")

class UpdateRaceTimeViewTests(TestCase):
    def setUp(self):
        #Set up test data: Create a user, race, and race entry.
            self.USERNAME = "test_user"
            self.PASSWORD = "password123"
            self.user = User.objects.create_user(username=self.USERNAME, password=self.PASSWORD)
            loc1 = Location.objects.create(name="Forum (North)", latitude=50.735836, longitude=-3.533852)
            loc2 = Location.objects.create(name="Armory (A)", latitude=50.736859, longitude=-3.531877)
            self.race = Race.objects.create(title="Test Race", start=loc1, end=loc2)
            self.entry = RaceEntry.objects.create(race=self.race, user=self.user, start_time=now(), end_time=now()+timedelta(minutes=10))
            self.url = reverse("update_race_time")

    def test_update_race_time_success_new_PB(self):
        #Test updating race time when new PB is set.
        self.client.login(username=self.USERNAME, password=self.PASSWORD)

        start_time = now()
        end_time = start_time + timedelta(minutes=6)  
        attempt_duration = (end_time - start_time).total_seconds()

        data = {
            "race_id": self.race.id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }

        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        
        # Reload entry from database
        self.entry.refresh_from_db()
        DB_duration = RaceEntry.objects.filter(user=self.user, race=self.race).first().get_duration()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(attempt_duration, DB_duration)

    def test_update_race_time_success_not_new_PB(self):
        #Test request response and DB structure when a new PB is not attained.
        self.client.login(username=self.USERNAME, password=self.PASSWORD)

        start_time = now()
        end_time = start_time + timedelta(minutes=15)  
        attempt_duration = (end_time - start_time).total_seconds()

        data = {
            "race_id": self.race.id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }

        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        
        # Reload entry from database
        self.entry.refresh_from_db()
        DB_duration = RaceEntry.objects.filter(user=self.user, race=self.race).first().get_duration()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertNotEqual(attempt_duration, DB_duration)
   
    def test_update_race_time_Race_not_found(self):
        self.client.login(username=self.USERNAME, password=self.PASSWORD)

        #Test when the Race does not exist.
        data = {
            "race_id": -1, #Race ID does not link to race
            "start_time": now().isoformat(),
            "end_time": (now() + timedelta(minutes=6)).isoformat()
        }

        response = self.client.post(self.url, json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["status"], "error")
        self.assertEqual(response.json()["message"], "Race not found")


        
class RestrictedUrlRaceRedirectTests(TestCase):
    def setUp(self):
        # Create test Race to provide race-detail page to query for redirect  
        loc1 = Location.objects.create(name="Forum (North)", latitude=50.735836, longitude=-3.533852)
        loc2 = Location.objects.create(name="Armory (A)", latitude=50.736859, longitude=-3.531877)
        self.race1 = Race.objects.create(title="Race 1", start=loc1, end=loc2)


    def test_race_menu_redirect_on_unauthorized_request(self):

        response = self.client.get(reverse("race"))  

        self.assertEqual(response.status_code, 302)

    def test_race_detail_redirect_on_unauthorized_request(self):

        response = self.client.get(reverse("race_detail", kwargs={"race_id": 1}))  

        self.assertEqual(response.status_code, 302)

    #Test when the User does not exist.
    def test_update_race_time_user_not_logged_in(self):
        loc1 = Location.objects.create(name="Forum (North)", latitude=50.735836, longitude=-3.533852)
        loc2 = Location.objects.create(name="Armory (A)", latitude=50.736859, longitude=-3.531877)
        race = Race.objects.create(title="Test Race", start=loc1, end=loc2)
        url = reverse("update_race_time")
        data = {
            "race_id": race.id,
            "start_time": now().isoformat(),
            "end_time": (now() + timedelta(minutes=6)).isoformat()
        }

        response = self.client.post(url, json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 302)


class RacePageTest(TestCase):
    def setUp(self):
        # Create test Race objects 
        loc1 = Location.objects.create(name="Forum (North)", latitude=50.735836, longitude=-3.533852)
        loc2 = Location.objects.create(name="Armory (A)", latitude=50.736859, longitude=-3.531877)
        self.race1 = Race.objects.create(title="Race 1", start=loc1, end=loc2)
        # User needed for authorised get request 
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_race_details_page_loads(self):
        # Login the test user
        self.client.login(username='testuser', password='password')
        
        # Use reverse to get the correct URL
        response = self.client.get(reverse('race_detail', kwargs={'race_id': self.race1.id}))
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        # Check template used
        self.assertTemplateUsed(response, 'race/race.html')

class ExeploreTests(TestCase):

    def setUp(self):
        self.username = 'raceuser'
        self.password = 'raceuserpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.client.login(username=self.username, password=self.password)

        self.start_location = Location.objects.create(name="Start", latitude=0.0, longitude=0.0)
        self.end_location = Location.objects.create(name="Finish", latitude=1.0, longitude=1.0)

        self.race = Race.objects.create(
            title='100m Dash',
            start=self.start_location,
            end=self.end_location,
            medal_requirements=[10, 20, 30]
        )

    def test_add_exeplore_points_valid_user(self):
        request_data = {
            "user": self.username,
            "start_latitude": 0.0,
            "start_longitude": 0.0,
            "end_latitude": 1.0,
            "end_longitude": 1.0,
        }

        response = self.client.post(reverse('add_exeplore_points'),
                                    json.dumps(request_data),
                                    content_type='application/json',)

        self.assertEqual(response.status_code, 200)
        self.assertIn('points', response.json())
        added_points = response.json()['points']

        self.profile.refresh_from_db()

        self.assertEqual(self.profile.points, int(added_points))

    def test_add_exeplore_points_user_not_found(self):
        request_data = {
            "user": "nonexistentuser",
            "start_latitude": 0.0,
            "start_longitude": 0.0,
            "end_latitude": 1.0,
            "end_longitude": 1.0,
        }

        response = self.client.post(reverse('add_exeplore_points'),
                                     json.dumps(request_data),
                                     content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['status'], "error")
        self.assertEqual(response.json()['message'], "User not found")

    def test_add_exeplore_points_invalid_request_method(self):
        response = self.client.get(reverse('add_exeplore_points'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], "error")
        self.assertEqual(response.json()['message'], "Invalid request method")
