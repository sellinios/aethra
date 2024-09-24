from django.urls import path
from .views.view_geography_planet import planet_count, health_check
from .views.view_geography_municipality import MunicipalityList  # Import MunicipalityList

urlpatterns = [
    path('planet-count/', planet_count, name='planet_count'),  # API endpoint for planet count
    path('health/', health_check, name='health_check'),  # Health check endpoint
    path('municipalities/', MunicipalityList.as_view(), name='municipality-list'),  # API endpoint for municipalities
]
