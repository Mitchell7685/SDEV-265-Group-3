from django.urls import path, include
from . import views

urlpatterns = [
    # Home Page (Dashboard)
    path("", views.home, name="home"),

    # Django's Built-in Login/Logout URLs
    # This handles /accounts/login and logout/
    path("accounts/", include("django.contrib.auth.urls")),

    # Our Custom Signup URL
    path("accounts/signup/", views.signup, name="signup"),
]
