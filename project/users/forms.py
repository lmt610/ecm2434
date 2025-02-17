from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(validators=[EmailValidator()])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
