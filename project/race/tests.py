import json
from django.test import TestCase
from django.urls import reverse

class RaceViewTest(TestCase):

    def setUp(self):
        self.url = reverse("calculate_distance")

    def test_calculate_distance_within_range(self):
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
        data = {
            "latitude": 40.712776,
            "longitude": -74.005974,
            "targetLatitude": -40.713800,  
            "targetLongitude": 74.006900
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "outside range")
