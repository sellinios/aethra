# api/views/view_geography_place.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from geography.models.model_geographic_place import GeographicPlace
from geography.models.model_geographic_division import GeographicDivision
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.utils.translation import get_language
import logging
import math

# Configure logging
logger = logging.getLogger(__name__)

# Lapse rate for temperature adjustment (degrees Celsius per meter)
LAPSE_RATE_C_PER_METER = 0.006  # 0.6°C per 100 meters

# Function to convert temperature and adjust for elevation
def convert_and_adjust_temperature(kelvin_temp, elevation):
    if kelvin_temp is not None:
        # Convert Kelvin to Celsius
        celsius_temp = kelvin_temp - 273.15
        # Adjust for elevation using lapse rate
        adjusted_temp = celsius_temp - (elevation * LAPSE_RATE_C_PER_METER)
        # Round the temperature
        return round(adjusted_temp)
    else:
        return None

# Parameter mapping
PARAMETER_MAPPING = {
    # ... your existing parameter mappings ...
}

# Function to calculate wind speed and direction
def calculate_wind(u, v):
    if u is not None and v is not None:
        # Wind speed in m/s
        wind_speed = math.sqrt(u ** 2 + v ** 2)
        wind_speed = round(wind_speed, 2)

        # Wind direction in degrees
        wind_dir_radians = math.atan2(-u, -v)
        wind_dir_degrees = math.degrees(wind_dir_radians)
        wind_dir_degrees = (wind_dir_degrees + 360) % 360  # Ensure value is between 0 and 360

        # Convert wind direction to compass direction
        compass_sectors = [
            "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
        ]
        idx = int((wind_dir_degrees + 11.25) / 22.5) % 16
        wind_direction = compass_sectors[idx]

        # Convert wind speed to Beaufort scale
        beaufort_scale = [
            (0, 0.3, 0),
            (0.3, 1.6, 1),
            (1.6, 3.4, 2),
            (3.4, 5.5, 3),
            (5.5, 8.0, 4),
            (8.0, 10.8, 5),
            (10.8, 13.9, 6),
            (13.9, 17.2, 7),
            (17.2, 20.8, 8),
            (20.8, 24.5, 9),
            (24.5, 28.5, 10),
            (28.5, 32.7, 11),
            (32.7, float('inf'), 12)
        ]
        beaufort = next((b for min_s, max_s, b in beaufort_scale if min_s <= wind_speed < max_s), 0)

        return wind_speed, wind_direction, beaufort
    else:
        return None, None, None

# Function to calculate probability of storm
def calculate_storm_probability(conv_precip_rate):
    if conv_precip_rate is not None:
        if conv_precip_rate == 0:
            return 0
        elif conv_precip_rate < 0.0001:
            return 20
        elif conv_precip_rate < 0.0005:
            return 40
        elif conv_precip_rate < 0.001:
            return 60
        elif conv_precip_rate < 0.005:
            return 80
        else:
            return 100
    else:
        return None

def get_weather_data_for_place(place):
    # Implement your weather data retrieval logic here
    # For simplicity, return an empty list if not implemented
    weather_data = []
    return weather_data

def place_detail(request, country_slug=None, region_slug=None, municipality_slug=None, place_slug=None):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    language = get_language()

    if latitude and longitude:
        # Handle geolocation-based request
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Invalid latitude or longitude.'}, status=400)

        user_location = Point(longitude, latitude, srid=4326)

        # Find the nearest place
        place = GeographicPlace.objects.annotate(
            distance=Distance('location', user_location)
        ).order_by('distance').first()

        if not place:
            return JsonResponse({'error': 'No places found.'}, status=404)

        # Fetch weather data
        weather_data = get_weather_data_for_place(place)

        # Include slugs and names in the response
        response_data = {
            'name': place.safe_translation_getter('name', language_code=language, any_language=True),
            'description': place.safe_translation_getter('description', language_code=language, any_language=True),
            'latitude': place.latitude,
            'longitude': place.longitude,
            'elevation': place.elevation,
            'continent_slug': place.get_continent_slug(language),
            'country_slug': place.get_country_slug(language),
            'region_slug': place.get_region_slug(language),
            'municipality_slug': place.admin_division.safe_translation_getter('slug', language_code=language,
                                                                              any_language=True),
            'municipality_name': place.admin_division.safe_translation_getter('name', language_code=language,
                                                                              any_language=True),
            'place_slug': place.safe_translation_getter('slug', language_code=language, any_language=True),
        }

        return JsonResponse(response_data)
    else:
        # Ensure all required URL parameters are present
        if not all([country_slug, region_slug, municipality_slug, place_slug]):
            return JsonResponse({'error': 'Missing required URL parameters.'}, status=400)

        # Get the municipality
        try:
            municipality = GeographicDivision.objects.translated(language_code=language).get(
                slug=municipality_slug
            )
        except GeographicDivision.DoesNotExist:
            return JsonResponse({'error': 'Municipality not found.'}, status=404)

        # Find the place
        try:
            place = GeographicPlace.objects.translated(language_code=language).get(
                translations__slug=place_slug,
                admin_division=municipality
            )
        except GeographicPlace.DoesNotExist:
            return JsonResponse({'error': 'Place not found.'}, status=404)

        # Fetch weather data
        weather_data = get_weather_data_for_place(place)

        response_data = {
            'name': place.safe_translation_getter('name', language_code=language, any_language=True),
            'description': place.safe_translation_getter('description', language_code=language, any_language=True),
            'latitude': place.latitude,
            'longitude': place.longitude,
            'elevation': place.elevation,
            'weather_data': weather_data,
        }

        return JsonResponse(response_data)
