from django.test import TestCase
from ..forms import LoginForm, UserRegistrationForm
from django.forms import CharField, PasswordInput

class LoginFormTest(TestCase):
    def setUp(self):
        self.form = LoginForm()

    def test_field_names(self):
        self.assertEqual(sorted(self.form.fields.keys()), ["password", "username"])

    def test_password_field(self):
        password_field = self.form.fields["password"]
        self.assertIsInstance(password_field, CharField)
        self.assertIsInstance(password_field.widget, PasswordInput)

class UserRegistrationFormTest(TestCase):
    def setUp(self):
        self.form = UserRegistrationForm()

    def test_field_names(self):
        self.assertEqual(sorted(self.form.fields.keys()), ["email", "password", "username"])

    def test_password_field(self):
        password_field = self.form.fields["password"]
        self.assertIsInstance(password_field, CharField)
        self.assertIsInstance(password_field.widget, PasswordInput)
