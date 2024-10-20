# api/urls.py

from django.urls import path
from .views.view_geography_planet import planet_count, planet_list
from .views.view_geography_municipalities import MunicipalityList
from .views.view_geography_place import place_detail
from .views.view_geography_nearest_place import nearest_place
from .views.view_weather_for_place import weather_for_place
from .views.view_weather_for_place_daily import weather_for_place_daily
from api.views.view_articles import ArticlesArticleListView, ArticlesArticleDetailView

urlpatterns = [
    path('planet-count/', planet_count, name='planet_count'),
    path('planet-list/', planet_list, name='planet_list'),
    path('municipalities/', MunicipalityList.as_view(), name='municipality-list'),
    path('place/', nearest_place, name='nearest_place'),
    path('weather/<slug:place_slug>/', weather_for_place, name='weather_for_place'),
    path(
        'weather/daily/<slug:place_slug>/',
        weather_for_place_daily,
        name='weather_for_place_daily'  # New URL for daily weather
    ),
    path(
        '<slug:country_slug>/<slug:region_slug>/<slug:municipality_slug>/<slug:place_slug>/',
        place_detail,
        name='place_detail'
    ),
    # Article-related API paths
    path('news/', ArticlesArticleListView.as_view(), name='news-api'),
    path('news/<slug:slug>/', ArticlesArticleDetailView.as_view(), name='news-detail-api'),
]
