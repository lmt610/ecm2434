from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ..forms import LoginForm

class LoginViewTest(TestCase):
    __USER_NAME = "testUser"
    __USER_PASSWORD = "testPassword192"

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username=self.__USER_NAME, password=self.__USER_PASSWORD)

    def test_get_page(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], LoginForm)
        self.assertFalse(response.context['form'].is_bound) 

    def test_valid_sign_in(self):
        response = self.client.post("/login/", {"username": self.__USER_NAME, "password":self.__USER_PASSWORD})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("welcome"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_wrong_username(self):
        response = self.client.post("/login/", {"username": "wrongUsername", "password":self.__USER_PASSWORD})
        self.assert_login_failed(response)        

    def test_wrong_password(self):
        response = self.client.post("/login/", {"username": self.__USER_NAME, "password":"wrongPassword"})
        self.assert_login_failed(response)

    def test_wrong_form_format(self):
        wrong_forms = [
            {},
            {"otherAttrib":12},
            {"usr":self.__USER_NAME, "password": self.__USER_PASSWORD},
            {"username":["harry", 12], "password": {"random":["james", "simon"]}}
        ] 
        for form in wrong_forms:
            response = self.client.post("/login/", form)
            self.assert_login_failed(response) 

    def assert_login_failed(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
