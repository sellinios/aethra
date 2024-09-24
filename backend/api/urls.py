# backend/api/urls.py

from django.urls import path
from . import views  # Import the views module from the current directory

urlpatterns = [
    path('planet-count/', views.planet_count, name='planet_count'),  # API endpoint for planet count
    path('health/', views.health_check, name='health_check'),  # Health check endpoint
]
