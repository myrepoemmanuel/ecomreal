from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    # class Meta:
    #     model = User
    #     fields = ['user_name','full_name', 'email', 'password1', 'password2']
        
