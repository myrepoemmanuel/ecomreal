from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Categories)
admin.site.register(Featuredproduct)
admin.site.register(ShippingAddress)
admin.site.register(BrandCategories)
admin.site.register(BrandMiniCategories)