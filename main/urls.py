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

    # Admin Schedule Generator
    path('generate-schedule/', views.generate_schedule, name='generate_schedule'),

    # Admin Delete Chore
    path('admin-delete-chore/<int:chore_id>/', views.admin_delete_chore, name='admin_delete_chore'),
    
    # User Complete Chore
    path('complete-chore/<int:assignment_id>/', views.complete_chore, name='complete_chore'),
]
