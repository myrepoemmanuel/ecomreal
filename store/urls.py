from django.urls import path
from . import views


urlpatterns = [
#    path('', views.index, name="index"),
    path('', views.store, name="store"),
    path('about/', views.about, name="about"),
    path('contacts/', views.contact, name="site-cont"),
    path('store/<slug:slug>', views.brandNames, name="site-brands"),
    
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('process_images/', views.processImages, name="process_images"),
]