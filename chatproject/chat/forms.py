from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Room,Message

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ['host']

class SignUpform(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']


class ProfileForm(UserCreationForm):
    password1=None
    password2=None
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']
        
     