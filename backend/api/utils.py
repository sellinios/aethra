# api/utils.py

import math
import logging
from datetime import datetime, timedelta
from django.utils import timezone
from weather.models import GFSForecast

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
        return round(adjusted_temp, 2)
    else:
        return None

# Function to calculate wind speed and direction
def calculate_wind(u, v):
    if u is not None and v is not None:
        # Wind speed in m/s
        wind_speed = math.sqrt(u ** 2 + v ** 2)
        wind_speed = round(wind_speed, 2)

        # Wind direction in degrees
        wind_dir_radians = math.atan2(-u, -v)
        wind_dir_degrees = (math.degrees(wind_dir_radians) + 360) % 360  # Ensure value is between 0 and 360

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

# Function to get weather data for a place
def get_weather_data_for_place(place):
    # Define the time range for the forecast
    now = timezone.now()
    start_date = now.date()
    end_date = start_date + timedelta(days=7)  # Adjust the range as needed

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
        storm_probability = calculate_storm_probability(conv_precip_rate)

        # Convert pressure from Pa to hPa
        pressure_hPa = pressure_Pa / 100.0 if pressure_Pa is not None else None

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
            'pressure_hPa': round(pressure_hPa, 2) if pressure_hPa else None,
            # Include other fields as needed
        }

        weather_data.append(weather_entry)

    return weather_data
