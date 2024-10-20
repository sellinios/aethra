# api/utils/alerts.py

def generate_alerts_for_weather(place, weather_entry):
    """
    Generate alerts based on the latest weather data for a place.

    Parameters:
    - place (GeographicPlace): The place for which to generate alerts.
    - weather_entry (dict): The latest weather data entry.

    Returns:
    - list: A list of alert dictionaries.
    """
    alerts = []

    temperature = weather_entry.get('temperature_celsius')
    wind_speed = weather_entry.get('wind_speed_m_s')
    precipitation = weather_entry.get('total_precipitation_mm')
    storm_probability = weather_entry.get('storm_probability_percent')
    flood = weather_entry.get('flood')

    # High Temperature Alert
    if temperature and temperature > 35:
        alerts.append({
            "title": "High Temperature",
            "description": f"Temperature has reached {temperature}°C.",
            "level": "WARNING"
        })

    # Severe Wind Alert
    if wind_speed and wind_speed > 40:
        alerts.append({
            "title": "Severe Wind",
            "description": f"Wind speed is {wind_speed} m/s.",
            "level": "SEVERE"
        })

    # Heavy Precipitation Alert
    if precipitation and precipitation > 100:
        alerts.append({
            "title": "Heavy Precipitation",
            "description": f"Precipitation rate is {precipitation} mm.",
            "level": "WARNING"
        })

    # Flood Alert
    if flood == 'Flood':
        alerts.append({
            "title": "Flood Risk",
            "description": "High risk of flooding due to heavy precipitation and storm conditions.",
            "level": "SEVERE"
        })

    # Add more alert conditions as needed

    return alerts  # Return the list of alert dictionaries
