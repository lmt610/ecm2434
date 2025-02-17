from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class LoginViewTest(TestCase):
    __USER_NAME = "testUser"
    __USER_PASSWORD = "testPassword192"

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username=self.__USER_NAME, password=self.__USER_PASSWORD)

    def test_valid_sign_in(self):
        response = self.client.post("/login/", {"username": self.__USER_NAME, "password":self.__USER_PASSWORD})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("welcome"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_wrong_username(self):
        response = self.client.post("/login/", {"username": "wrongUsername", "password":self.__USER_PASSWORD})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
