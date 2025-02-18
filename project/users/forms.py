from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=65, required=True)
    password = forms.CharField(max_length=65, required=True, widget=forms.PasswordInput)
    email = forms.EmailField(max_length=65, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password and len(password)<8:
            raise forms.ValidationError("Password must be at least 8 characters")

        return password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists")

        return email
