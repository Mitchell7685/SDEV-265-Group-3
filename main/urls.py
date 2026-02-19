from django.urls import path, include
from . import views
from .views import manage_extensions, request_extension

urlpatterns = [
    # Home Page (Dashboard)
    path("", views.home, name="home"),

    # Django's Built-in Login/Logout URLs
    # This handles /accounts/login and logout/
    path("accounts/", include("django.contrib.auth.urls")),

    # Our Custom Signup URL
    path("accounts/signup/", views.signup, name="signup"),

    # Admin Schedule Generator
    path('generate-schedule/', views.generate_schedule, name='generate_schedule'),
    path('chore/<int:chore_id>/request-extension/', request_extension, name='request_extension'),
    path('admin/manage-extensions/', manage_extensions, name='manage_extensions'),
]    