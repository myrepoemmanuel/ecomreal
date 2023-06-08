from dataclasses import fields
from django import forms
from django.forms import ModelForm
from .models import Vendor
from store.models import Products, Categories
# from django.contrib.auth.forms import UserCreationForm


class AddProducts(ModelForm):
    # required_css_class = 'required'
    email = forms.EmailField()

    class Meta:
        model = Products
        # fields = ['email', 'name', 'price', 'Brand', 'description', 'digital', 'image', 'image2', 'image3', 'image4']
        fields = '__all__'
        exclude = ("vendor",)