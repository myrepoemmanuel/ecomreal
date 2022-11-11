from django.urls import path
from . import views

app_name = 'vendors'

urlpatterns = [
    path("dashboard", views.vendor_dash, name="vendor_dash"),
    path("add_product", views.add_product, name="add_product"),
    path("shop/<slug:slug>", views.my_shop, name="my_shop"),
    path("shop/notVendor", views.my_shop, name="my_shop"),
    path("shop/<str:str>/<slug:slug>", views.vendor_categories, name="vendor_categories"),
    

]