# api/utils/weather_data.py

import math
import logging
from datetime import datetime, timedelta, timezone  # Import timezone from datetime
from django.utils import timezone as django_timezone  # Alias to avoid confusion
from django.db.models import Max, Min, Avg, FloatField
from django.db.models.functions import TruncDate, Cast
from geography.models import GeographicPlace
from weather.models import GFSForecast
from .wind import calculate_wind, calculate_alert_probability  # Ensure this line is present
from .alerts import generate_alerts_for_weather
from .day_night import is_daytime
from .weather_state import determine_weather_state

# Configure logging
logger = logging.getLogger(__name__)

# Constants
LAPSE_RATE_C_PER_METER = 0.006  # 0.6°C per 100 meters

def convert_and_adjust_temperature(kelvin_temp, elevation):
    if kelvin_temp is not None:
        # Convert Kelvin to Celsius
        celsius_temp = kelvin_temp - 273.15
        # Adjust for elevation using lapse rate
        adjusted_temp = celsius_temp - (elevation * LAPSE_RATE_C_PER_METER)
        # Round the temperature
        return round(adjusted_temp, 2)
    return None

def calculate_pressure_hpa(pressure_pa):
    return round(pressure_pa / 100.0, 2) if pressure_pa is not None else None

def get_weather_data_for_place(place):
    """
    Fetch and process weather data for a given place.
    """
    # Define the time range for the forecast (e.g., next 7 days)
    now = django_timezone.now()
    start_date = now.date()
    end_date = start_date + timedelta(days=7)  # Adjust as needed

    # Query GFSForecast data for the place and date range
    forecasts = GFSForecast.objects.filter(
        place=place,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date', 'hour')

    weather_data = []

    for forecast in forecasts:
        # Extract forecast data from the JSONField
        forecast_data = forecast.forecast_data

        # Build a datetime object from the date and hour
        forecast_datetime = datetime.combine(forecast.date, datetime.min.time()) + timedelta(hours=forecast.hour)
        # Make forecast_datetime timezone-aware using Python's datetime.timezone.utc
        forecast_datetime = django_timezone.make_aware(forecast_datetime, timezone=timezone.utc)

        # Extract necessary fields from forecast_data
        temperature_kelvin = forecast_data.get('2t_level_2_heightAboveGround')
        relative_humidity_percent = forecast_data.get('2r_level_2_heightAboveGround')
        total_precipitation_mm = forecast_data.get('tp_level_0_surface')
        conv_precip_rate = forecast_data.get('cprat_level_0_surface')
        wind_u = forecast_data.get('10u_level_10_heightAboveGround')
        wind_v = forecast_data.get('10v_level_10_heightAboveGround')
        pressure_Pa = forecast_data.get('prmsl_level_0_meanSea')  # Pressure in Pascals

        # Adjust temperature for elevation
        adjusted_temp_celsius = convert_and_adjust_temperature(
            kelvin_temp=temperature_kelvin,
            elevation=place.elevation
        )

        # Calculate wind properties
        wind_speed, wind_direction, beaufort_scale = calculate_wind(wind_u, wind_v)

        # Calculate storm probability
        storm_probability = calculate_alert_probability(conv_precip_rate)

        # Convert pressure from Pa to hPa
        pressure_hPa = calculate_pressure_hpa(pressure_Pa)

        # Determine day or night
        day_or_night = is_daytime(forecast_datetime, place.latitude, place.longitude)

        # Determine weather state
        weather_state = determine_weather_state({
            'temperature_celsius': adjusted_temp_celsius,
            'total_precipitation_mm': total_precipitation_mm,
            'avg_cloud_cover': forecast_data.get('lcc_level_0_lowCloudLayer', 0),
            'wind_speed_m_s': wind_speed,
            'storm_probability_percent': storm_probability,
            'flood': 'Flood' if storm_probability >= 80 else 'No Flood',
        })

        # Build the weather data entry
        weather_entry = {
            'datetime': forecast_datetime.isoformat(),
            'temperature_celsius': adjusted_temp_celsius,
            'relative_humidity_percent': relative_humidity_percent,
            'wind_speed_m_s': wind_speed,
            'wind_direction': wind_direction,
            'wind_beaufort_scale': beaufort_scale,
            'total_precipitation_mm': total_precipitation_mm,
            'storm_probability_percent': storm_probability,
            'pressure_hPa': pressure_hPa,
            'day_or_night': day_or_night,
            'weather_state': weather_state,
            # Include other fields as needed
        }

        weather_data.append(weather_entry)

    return weather_data

def get_daily_weather_data_for_place(place):
    """
    Fetch and aggregate daily weather data for a given place.
    """
    today = django_timezone.now().date()
    logger.debug(f"Today's date: {today}")

    # Fetch and aggregate daily weather data from GFSForecast
    daily_forecasts = (
        GFSForecast.objects.filter(place=place, date__gte=today)
        .annotate(date_only=TruncDate('date'))
        .values('date_only')
        .annotate(
            max_temp=Max(Cast('forecast_data__2t_level_2_heightAboveGround', FloatField())),
            min_temp=Min(Cast('forecast_data__2t_level_2_heightAboveGround', FloatField())),
            avg_cloud_cover=Avg(Cast('forecast_data__lcc_level_0_lowCloudLayer', FloatField())),
            max_precipitation=Max(Cast('forecast_data__tp_level_0_surface', FloatField())),
            wind_speed_avg=Avg(Cast('forecast_data__10u_level_10_heightAboveGround', FloatField())),
        )
        .order_by('date_only')
    )

    logger.debug(f"Number of daily forecasts fetched: {daily_forecasts.count()}")

    # Reconstruct the date from the extracted date_only
    daily_weather_data = [
        {
            'date': forecast['date_only'].strftime('%Y-%m-%d') if forecast.get('date_only') else None,
            'max_temp': (forecast['max_temp'] - 273.15) if forecast.get('max_temp') is not None else None,
            'min_temp': (forecast['min_temp'] - 273.15) if forecast.get('min_temp') is not None else None,
            'avg_cloud_cover': forecast.get('avg_cloud_cover'),
            'max_precipitation': forecast.get('max_precipitation'),
            'wind_speed_avg': forecast.get('wind_speed_avg'),
        }
        for forecast in daily_forecasts
    ]

    logger.debug(f"Processed daily weather data: {daily_weather_data}")

    return daily_weather_data
