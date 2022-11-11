from django.urls import path
from django.conf.urls import include
from . import views
from vendors.views import process_vendor
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name="site-register"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name="site-profile"),
    path('changePassword', views.change_password, name='change_password'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name="site-login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name="site-logout"),

    path('process_profile/', views.process_profile, name="process_profile"),
    path("process_vendor/", process_vendor, name="process_vendor")
   
]