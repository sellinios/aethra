# api/views/view_geography_place.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from geography.models.model_geographic_place import GeographicPlace
from geography.models.model_geographic_division import GeographicDivision
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from weather.models.model_gfs_forecast import GFSForecast
from django.utils import timezone
from datetime import datetime, timedelta, timezone as dt_timezone
from django.db.models import Max, OuterRef, Subquery, F
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Parameter mapping
PARAMETER_MAPPING = {
    '2t_level_2_heightAboveGround': {
        'name': 'temperature_celsius',
        'conversion': lambda k: round(k - 273.15, 2) if k is not None else None  # Convert Kelvin to Celsius
    },
    'r_level_2_heightAboveGround': {
        'name': 'relative_humidity_percent',
        'conversion': lambda r: round(r, 2) if r is not None else None  # Relative Humidity in %
    },
    'wind_speed_gust_surface': {
        'name': 'wind_gust_speed_m_s',
        'conversion': lambda x: round(x, 2) if x is not None else None  # Wind gust speed in m/s
    },
    '10u_level_10_heightAboveGround': {
        'name': 'u_component_wind_m_s',
        'conversion': lambda x: round(x, 2) if x is not None else None  # U-component of wind at 10 meters (m/s)
    },
    '10v_level_10_heightAboveGround': {
        'name': 'v_component_wind_m_s',
        'conversion': lambda x: round(x, 2) if x is not None else None  # V-component of wind at 10 meters (m/s)
    },
    'tp_level_0_surface': {
        'name': 'total_precipitation_mm',
        'conversion': lambda tp: round(tp, 2) if tp is not None else None  # Total precipitation in mm
    },
    'sp_level_0_surface': {
        'name': 'surface_pressure_hPa',
        'conversion': lambda p: round(p / 100.0, 2) if p is not None else None  # Surface Pressure in hPa
    },
    'meanSea': {
        'name': 'mean_sea_level_pressure_hPa',
        'conversion': lambda p: round(p / 100.0, 2) if p is not None else None  # Pressure reduced to MSL in hPa
    },
    'convective_precipitation_rate_surface': {
        'name': 'convective_precipitation_rate',
        'conversion': lambda x: round(x, 2) if x is not None else None  # Convective precipitation rate
    },
    'high_cloud_cover_highCloudLayer': {
        'name': 'high_cloud_cover',
        'conversion': lambda x: round(x, 2) if x is not None else None  # High cloud cover
    },
    'low_cloud_cover_lowCloudLayer': {
        'name': 'low_cloud_cover',
        'conversion': lambda x: round(x, 2) if x is not None else None  # Low cloud cover
    },
    'medium_cloud_cover_middleCloudLayer': {
        'name': 'medium_cloud_cover',
        'conversion': lambda x: round(x, 2) if x is not None else None  # Medium cloud cover
    },
    'precipitation_rate_surface': {
        'name': 'precipitation_rate',
        'conversion': lambda x: round(x, 2) if x is not None else None  # Precipitation rate
    },
}




def place_detail(request, country_slug=None, region_slug=None, municipality_slug=None, place_slug=None):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

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

        # Include slugs in the response
        response_data = {
            'name': place.safe_translation_getter('name'),
            'description': place.safe_translation_getter('description'),
            'latitude': place.latitude,
            'longitude': place.longitude,
            'elevation': place.elevation,
            'continent_slug': 'europe',  # Adjust if necessary
            'country_slug': place.get_country_slug(),
            'region_slug': place.get_region_slug(),
            'municipality_slug': place.admin_division.slug,
            'place_slug': place.safe_translation_getter('slug'),
            'weather_data': weather_data,
        }

        return JsonResponse(response_data)
    else:
        # Existing logic to get place by slugs
        if not all([country_slug, region_slug, municipality_slug, place_slug]):
            return JsonResponse({'error': 'Missing required URL parameters.'}, status=400)

        admin_division = get_object_or_404(
            GeographicDivision.objects.language().filter(slug=municipality_slug)
        )

        places = GeographicPlace.objects.language().filter(
            translations__slug=place_slug,
            admin_division=admin_division
        )

        if not places.exists():
            return JsonResponse({'error': 'Place not found.'}, status=404)

        place = places.first()

        # Fetch weather data
        weather_data = get_weather_data_for_place(place)

        response_data = {
            'name': place.safe_translation_getter('name'),
            'description': place.safe_translation_getter('description'),
            'latitude': place.latitude,
            'longitude': place.longitude,
            'elevation': place.elevation,
            'weather_data': weather_data,
        }

        return JsonResponse(response_data)

def get_weather_data_for_place(place):
    from django.db.models import Max, OuterRef, Subquery, F

    now = timezone.now()
    start_time = now - timedelta(hours=48)  # Show data starting from 48 hours in the past
    end_time = now + timedelta(hours=48)    # Show data up to 48 hours in the future

    # Step 1: Retrieve forecasts for the place within the extended date range
    forecasts = GFSForecast.objects.filter(
        place=place,
        date__gte=start_time.date(),
        date__lte=end_time.date()
    )

    # Step 2: Annotate forecasts with the latest 'utc_cycle_time' for each 'date' and 'hour'
    latest_cycles_subquery = GFSForecast.objects.filter(
        place=place,
        date=OuterRef('date'),
        hour=OuterRef('hour')
    ).values('date', 'hour').annotate(
        latest_utc_cycle_time=Max('utc_cycle_time')
    ).values('latest_utc_cycle_time')

    # Step 3: Filter forecasts to include only those with the latest 'utc_cycle_time'
    forecasts = forecasts.annotate(
        latest_utc_cycle_time=Subquery(latest_cycles_subquery)
    ).filter(
        utc_cycle_time=F('latest_utc_cycle_time')
    ).order_by('date', 'hour')

    weather_data = []

    for forecast in forecasts:
        forecast_datetime = datetime.combine(forecast.date, datetime.min.time()) + timedelta(hours=forecast.hour)
        forecast_datetime = forecast_datetime.replace(tzinfo=dt_timezone.utc)

        if start_time <= forecast_datetime <= end_time:
            weather_entry = {
                'datetime': forecast_datetime.isoformat(),
            }

            forecast_data = forecast.forecast_data

            # Collect all parameters
            for key, value in forecast_data.items():
                mapping = PARAMETER_MAPPING.get(key, {'name': key, 'conversion': lambda x: x})
                converted_value = mapping['conversion'](value)
                weather_entry[mapping['name']] = converted_value

            # Handle derived parameters (e.g., wind speed)
            if 'wind_u_component' in weather_entry and 'wind_v_component' in weather_entry:
                u = weather_entry['wind_u_component']
                v = weather_entry['wind_v_component']
                if u is not None and v is not None:
                    wind_speed = (u**2 + v**2)**0.5
                    weather_entry['wind_speed_m_s'] = round(wind_speed, 2)

            weather_data.append(weather_entry)

    # Sort the weather_data by datetime
    weather_data.sort(key=lambda x: x['datetime'])

    return weather_data
