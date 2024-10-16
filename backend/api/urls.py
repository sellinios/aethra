# api/urls.py

from django.urls import path
from .views.view_geography_planet import planet_count, planet_list
from .views.view_health import health_check
from .views.view_geography_ListMunicipality import MunicipalityList
from .views.view_geography_place import place_detail

urlpatterns = [
    path('planet-count/', planet_count, name='planet_count'),
    path('planet-list/', planet_list, name='planet_list'),
    path('health/', health_check, name='health_check'),
    path('municipalities/', MunicipalityList.as_view(), name='municipality-list'),
    path('place/', place_detail, name='place_detail_geolocation'),  # For geolocation-based requests
    path(
        '<slug:country_slug>/<slug:region_slug>/<slug:municipality_slug>/<slug:place_slug>/',
        place_detail,
        name='place_detail'
    ),
]
