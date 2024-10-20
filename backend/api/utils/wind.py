# api/utils/wind.py

import math


def calculate_wind(u, v):
    """
    Calculate wind speed, direction, and Beaufort scale.

    Parameters:
    - u (float): U-component of wind (m/s)
    - v (float): V-component of wind (m/s)

    Returns:
    - tuple: (wind_speed_m_s, wind_direction, beaufort_scale)
    """
    if u is not None and v is not None:
        # Wind speed in m/s
        wind_speed = math.sqrt(u ** 2 + v ** 2)
        wind_speed = round(wind_speed, 2)

        # Wind direction in degrees
        wind_dir_radians = math.atan2(-u, -v)
        wind_dir_degrees = (math.degrees(wind_dir_radians) + 360) % 360  # Ensure 0-360

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
    return None, None, None


def calculate_alert_probability(conv_precip_rate):
    """
    Calculate the probability of storm based on convective precipitation rate.

    Parameters:
    - conv_precip_rate (float): Convective precipitation rate

    Returns:
    - int: Probability percentage (0-100)
    """
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
    return None
