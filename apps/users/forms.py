from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "image", "bio", "display_real_name", "location", "display_location"]


class SubscribeForm(forms.Form):
    followed_user = forms.CharField(label=False, widget=forms.TextInput())
