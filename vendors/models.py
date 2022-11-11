from distutils.command.upload import upload
from itertools import product
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.


class Vendor(models.Model):
    vendor_name = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    shop_name = models.CharField(max_length=200, null=True, blank=True)
    shop_description = models.TextField(max_length=200, null=True, blank=True)
    shop_logo = models.ImageField(null=True, blank=True, upload_to="vendors")
    shop_location = models.CharField(max_length=200, null=True, blank=True)
    id_number = models.CharField(max_length=200, null=True, blank=True)
    dob = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.vendor_name}'

    @property
    def imageURL(self):
        try:
            url = self.shop_logo.url
        except:
            url = ''
        return url
    @property
    def shopName(self):
        try:
            shop = self.shop_name
        except:
            shop = ''
        return shop
