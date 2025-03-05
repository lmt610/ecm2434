from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from ..models import UserSettings

class SettingsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser12", password="testpassword")
        self.client.login(username="testuser12", password="testpassword")

    def test_valid_change_password(self):
        pass

    def test_invalid_change_password(self):
        pass

    def test_delete_account(self):
        pass

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
            {"setting": "location_tracking", "value": True},
            {"setting": "non existent attribute", "value": "true"}
        ]
        for form in invalid_forms:
            response = self.client.post("/toggle-setting/", form)
            self.assertEqual(response.status_code, 400)


    def test_contains_legal_info(self):
        response = self.client.get("/settings/")
        self.assertEqual(response.status_code, 200)
        
        soup = BeautifulSoup(response.content, 'html.parser')

        mandated_links = ["/privacy-policy/","/terms-of-service/", "/data-protection/"]
        
        for address in mandated_links:
            link = soup.find('a', href=address)
            self.assertIsNotNone(link)
