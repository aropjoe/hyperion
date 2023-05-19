from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Business
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email")


class BusinessRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Business
        fields = ("name", "email", "password")


class BusinessUpdateForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ("name", "email")
