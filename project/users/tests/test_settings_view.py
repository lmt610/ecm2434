from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from ..models import UserSettings
from django.urls import reverse
from django.contrib.messages import get_messages

class SettingsViewTest(TestCase):
    __USER_PASSWORD = "testpassword"

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser12", password=self.__USER_PASSWORD)
        self.client.login(username="testuser12", password="testpassword")

    def test_valid_change_password(self):
        form = {
            "old_password": self.__USER_PASSWORD,
            "new_password1": "newvalidpassword",
            "new_password2": "newvalidpassword"
        }
        response = self.client.post("/change-password/", form)
       
        self.assertEqual(response.json()["message"], "Your password was successfully updated!")
        self.assertFalse(User.objects.filter(password=self.user.password).exists())
        self.assertTrue(User.objects.filter(username=self.user.username).exists())

    def test_delete_account(self):
        response = self.client.post("/delete-account/")
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(len(messages),1)
        self.assertEqual(str(messages[0]), "Your account has been successfully deleted.")
        self.assertFalse(User.objects.filter(username=self.user.username).exists())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))

    def test_toggle_setting_valid(self):
        attributes = [field.name for field in UserSettings._meta.get_fields() if field.name not in ["id","user"]]
        
        for attribute in attributes:
            for value in ("false", "true"):
                response = self.client.post("/toggle-setting/", {"setting": attribute, "value":value})
                self.assertEqual(response.status_code, 200)
                settings = UserSettings.objects.get(user=self.user)
                self.assertEqual(getattr(settings, attribute), value=="true", f"Error: {attribute} value should be {value}")

    def test_toggle_setting_invalid(self):
        invalid_forms = [
            {},
            {"setting": "location_tracking"},
            {"value": "true"},
            {"setting": "non existent attribute", "value": "true"}
        ]
        for form in invalid_forms:
            response = self.client.post("/toggle-setting/", form)
            self.assertEqual(response.status_code, 400)


    def test_contains_links_to_legal_info(self):
        response = self.client.get("/settings/")
        self.assertEqual(response.status_code, 200)
        
        soup = BeautifulSoup(response.content, 'html.parser')

        links_text_list = ["Privacy Policy","Terms of Service", "Data Protection"]
        
        for link_text in links_text_list:
            link = soup.find('a', string=link_text)
            self.assertIsNotNone(link, f"Error: couldn't find {link_text}")
