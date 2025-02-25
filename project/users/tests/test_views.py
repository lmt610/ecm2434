from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ..forms import LoginForm, UserRegistrationForm

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
        self.assert_login_failed(response, "Invalid username or password")        

    def test_wrong_password(self):
        response = self.client.post("/login/", {"username": self.__USER_NAME, "password":"wrongPassword"})
        self.assert_login_failed(response, "Invalid username or password")

    def test_switch_user_passwords(self):
        user2_password = "otherValidPassword12"
        user2 = User.objects.create_user(username="otherUser", password=user2_password)
        
        response = self.client.post("/login/", {"username": self.__USER_NAME, "password":user2_password})
        self.assert_login_failed(response, "Invalid username or password")

    def test_wrong_form_format(self):
        missing_data_forms = [
            {},
            {"otherAttrib":12},
            {"usr":self.__USER_NAME, "password": self.__USER_PASSWORD},
        ]
        incorrect_data_forms = [
            {"username":["harry", 12], "password": {"random":["james", "simon"]}},
            {"username":"'@``\\'", "password":"\n\n\t\b\b\t\t"}
        ]

        for form in missing_data_forms:
            response = self.client.post("/login/", form)
            self.assert_login_failed(response, "This field is required") 

        for form in incorrect_data_forms:
            response = self.client.post("/login/", form)
            self.assert_login_failed(response, "Invalid username or password")

    def assert_login_failed(self, response, error_message):
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, error_message)

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_page(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UserRegistrationForm)
        self.assertFalse(response.context['form'].is_bound)

    def test_valid_sign_up(self):
        valid_form =  {
            "username": "validName",
            "email": "validemail@legit.com",
            "password": "validPassword182"
        }
        response = self.client.post('/register/', valid_form)
        new_user = User.objects.get(username=valid_form["username"])
        
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(valid_form["email"], new_user.email)
        hashPrefix = "pbkdf2_sha256$"
        self.assertEqual(hashPrefix, new_user.password[:len(hashPrefix)]) 
        self.assertEqual(response.url, reverse("welcome"))

    def test_duplicate_username(self):
        duplicate_username = "duplicateUsername"
        User.objects.create_user(username=duplicate_username, password="validPassword12", email="valid@email.com")
        invalid_form = {
            "username": duplicate_username,
            "password": "anotherValidPassword17",
            "email": "validAndUniquel@email.com"
        }
        self.assert_form_is_rejected(invalid_form, "A user with that username already exists")

    def test_duplicate_email(self):
        duplicate_email = "duplicate@email.com"
        User.objects.create_user(username="validUsername12", password="validPassword12", email=duplicate_email)
        invalid_form = {
            "username": "uniqueAndValidUsername",
            "password": "anotherValidPassword17",
            "email": duplicate_email
        }
        self.assert_form_is_rejected(invalid_form, "A user with that email already exists")

    def test_weak_password(self):
        invalid_form = {
            "username": "validUsername",
            "password": "weak",
            "email": "valid@email.com"
        }
        self.assert_form_is_rejected(invalid_form, "Password must be at least 8 characters")

    def test_wrong_form_format(self):
        valid_username = "HarrisonFord182"
        valid_password = "kjasdnf9889!"
        valid_email    = "michael@jackson.com"

        wrong_forms = [
            {},
            {"otherAttrib":12},
            {"username":valid_username, "password": valid_password},
            {"username":valid_username, "email": valid_email},
            {"password":valid_password, "email": valid_email},
            {"username":["harry", 12], "password": {"random":["james", "simon"]}, "email": {}}
        ] 
        for form in wrong_forms:
            response = self.client.post("/register/", form)
            self.assert_form_is_rejected(form, "This field is required")


    def assert_form_is_rejected(self, form, error_message):
        initial_user_count = User.objects.count()
        
        response = self.client.post("/register/", form)

        self.assertEqual(initial_user_count, User.objects.count())
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 200)
       
        self.assertContains(response, error_message) 

class RestrictedUrlUserRedirectTests(TestCase):
    def setUp(self):
        pass


    def test_welcome_redirect_on_unauthorized_request(self):

        response = self.client.get(reverse("welcome"))  

        self.assertEqual(response.status_code, 302)

    def test_settings_redirect_on_unauthorized_request(self):

        response = self.client.get(reverse("settings"))  

        self.assertEqual(response.status_code, 302)