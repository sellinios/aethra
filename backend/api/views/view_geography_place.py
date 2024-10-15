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
    '2t_level_2_heightAboveGround': {
        'name': 'temperature_celsius',
        # Use the conversion function that includes elevation adjustment
        'conversion': lambda k, elevation: convert_and_adjust_temperature(k, elevation)
    },
    '2r_level_2_heightAboveGround': {
        'name': 'relative_humidity_percent',
        'conversion': lambda r, **kwargs: round(r) if r is not None else None  # Relative Humidity in %
    },
    '10u_level_10_heightAboveGround': {
        'name': 'u_component_wind_m_s',
        'conversion': lambda x, **kwargs: x if x is not None else None  # U-component of wind at 10 meters (m/s)
    },
    '10v_level_10_heightAboveGround': {
        'name': 'v_component_wind_m_s',
        'conversion': lambda x, **kwargs: x if x is not None else None  # V-component of wind at 10 meters (m/s)
    },
    'tp_level_0_surface': {
        'name': 'total_precipitation_mm',
        'conversion': lambda tp, **kwargs: round(tp * 1000, 2) if tp is not None else None  # Convert from meters to mm
    },
    'prmsl_level_0_meanSea': {
        'name': 'mean_sea_level_pressure_hPa',
        'conversion': lambda p, **kwargs: round(p / 100.0) if p is not None else None  # Convert from Pa to hPa
    },
    'sp_level_0_surface': {
        'name': 'surface_pressure_hPa',
        'conversion': lambda p, **kwargs: round(p / 100.0) if p is not None else None  # Convert from Pa to hPa
    },
    'cprat_level_0_surface': {
        'name': 'convective_precipitation_rate',
        'conversion': lambda x, **kwargs: x if x is not None else None  # Convective precipitation rate (kg/m²/s)
    },
    'lcc_level_0_lowCloudLayer': {
        'name': 'low_cloud_cover_percent',
        'conversion': lambda x, **kwargs: round(x) if x is not None else None  # Low cloud cover in %
    },
    'mcc_level_0_middleCloudLayer': {
        'name': 'medium_cloud_cover_percent',
        'conversion': lambda x, **kwargs: round(x) if x is not None else None  # Medium cloud cover in %
    },
    'hcc_level_0_highCloudLayer': {
        'name': 'high_cloud_cover_percent',
        'conversion': lambda x, **kwargs: round(x) if x is not None else None  # High cloud cover in %
    },
    # Add other parameters as needed
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
        # Define thresholds for storm probability based on convective precipitation rate
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
    start_time = now  # Start from current time
    end_time = now + timedelta(hours=48)    # Show data up to 48 hours in the future

    # Step 1: Retrieve forecasts for the place within the date range
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
                mapping = PARAMETER_MAPPING.get(key, {'name': key, 'conversion': lambda x, **kwargs: x})
                # Adjust temperature using elevation
                if mapping['name'] == 'temperature_celsius':
                    converted_value = mapping['conversion'](value, elevation=place.elevation)
                else:
                    converted_value = mapping['conversion'](value)
                weather_entry[mapping['name']] = converted_value

            # Handle derived parameters (e.g., wind speed, direction, Beaufort scale)
            u = weather_entry.get('u_component_wind_m_s')
            v = weather_entry.get('v_component_wind_m_s')
            wind_speed, wind_direction, beaufort_scale = calculate_wind(u, v)
            weather_entry['wind_speed_m_s'] = wind_speed
            weather_entry['wind_direction'] = wind_direction
            weather_entry['wind_beaufort_scale'] = beaufort_scale

            # Remove raw u and v components
            weather_entry.pop('u_component_wind_m_s', None)
            weather_entry.pop('v_component_wind_m_s', None)

            # Calculate total cloud cover (sum of low, medium, high cloud cover)
            low_cloud = weather_entry.get('low_cloud_cover_percent')
            medium_cloud = weather_entry.get('medium_cloud_cover_percent')
            high_cloud = weather_entry.get('high_cloud_cover_percent')

            cloud_covers = [cc for cc in [low_cloud, medium_cloud, high_cloud] if cc is not None]
            total_cloud_cover = sum(cloud_covers)
            total_cloud_cover = min(total_cloud_cover, 100)  # Cap at 100%
            weather_entry['total_cloud_cover_percent'] = total_cloud_cover if cloud_covers else None

            # Handle surface pressure; if not available, use mean sea level pressure
            surface_pressure = weather_entry.get('surface_pressure_hPa')
            if surface_pressure is None:
                surface_pressure = weather_entry.get('mean_sea_level_pressure_hPa')
                weather_entry['pressure_hPa'] = surface_pressure
            else:
                weather_entry['pressure_hPa'] = surface_pressure

            # Remove individual pressure entries to avoid confusion
            weather_entry.pop('surface_pressure_hPa', None)
            weather_entry.pop('mean_sea_level_pressure_hPa', None)

            # Calculate probability of storm
            conv_precip_rate = weather_entry.get('convective_precipitation_rate')
            storm_probability = calculate_storm_probability(conv_precip_rate)
            weather_entry['storm_probability_percent'] = storm_probability

            weather_data.append(weather_entry)

    # Sort the weather_data by datetime
    weather_data.sort(key=lambda x: x['datetime'])

    return weather_data
