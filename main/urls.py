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

    # Admin Delete Chore
    path('admin-delete-chore/<int:chore_id>/', views.admin_delete_chore, name='admin_delete_chore'),
    
    # User Complete Chore
    path('complete-chore/<int:assignment_id>/', views.complete_chore, name='complete_chore'),

    # Request Extension
    path('chore/<int:chore_id>/request-extension/', request_extension, name='request_extension'),

    # Manage Extensions
    path('manage_extensions/', manage_extensions, name='manage_extensions'),
]