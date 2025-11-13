"""
URL Configuration for the bookmarks project.

This file maps URL patterns to views for the project, including:
- Admin panel
- User account management
- Social authentication
- Image management
- Debug toolbar (for development)
- Serving media files in development
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # User account management (login, logout, register, profile)
    path('account/', include('account.urls')),
    
    # Social authentication URLs (Facebook, Twitter, etc.)
    path('social-auth/', include('social_django.urls', namespace='social')),
    
    # Image app URLs (uploading, browsing, etc.)
    path('images/', include('images.urls', namespace='images')),
    
    # Debug toolbar URLs (only available in development)
    path('__debug__/', include("debug_toolbar.urls"))
]

# Serve media files in development (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
