# backend/backend/urls.py

from django.contrib import admin
from django.urls import path, include  # include to link to other app URLs

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface
    path('api/', include('api.urls')),  # Include API app's URLs
]
