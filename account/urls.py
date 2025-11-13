from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

# -------------------------------
# URL patterns for account app
# -------------------------------
urlpatterns = [
    # Include built-in Django authentication views
    # Provides: login, logout, password change/reset
    path('', include('django.contrib.auth.urls')),

    # Dashboard - main user page after login
    path('', views.dashboard, name='dashboard'),

    # User registration page
    path('register/', views.register, name='register'),

    # Edit logged-in user's profile
    path('edit/', views.edit, name='edit'),

    # List all users
    path('users/', views.user_list, name='user_list'),

    # Follow/unfollow functionality
    path('users/follow/', views.user_follow, name='user_follow'),

    # User detail page by username
    path('users/<username>/', views.user_detail, name='user_detail'),
]
