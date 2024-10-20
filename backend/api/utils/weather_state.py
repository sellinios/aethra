# api/utils/weather_state.py

def determine_weather_state(weather_entry):
    """
    Determine the weather state based on various weather parameters.

    Parameters:
    - weather_entry (dict): A dictionary containing weather parameters.

    Returns:
    - dict: A dictionary representing the weather state.
    """
    # Initialize default state
    state = {
        'temperature': 'Normal',
        'precipitation': 'None',
        'cloud_cover': 'Clear',
        'wind': 'Calm',
        'flood': 'No Flood',
    }

    # Temperature
    temperature = weather_entry.get('temperature_celsius')
    if temperature is not None:
        if temperature > 30:
            state['temperature'] = 'Hot'
        elif temperature < 0:
            state['temperature'] = 'Cold'

    # Precipitation
    total_precipitation = weather_entry.get('total_precipitation_mm')
    if total_precipitation is not None:
        if total_precipitation > 50:
            state['precipitation'] = 'Heavy Rain'
        elif total_precipitation > 0:
            state['precipitation'] = 'Rain'

    # Cloud Cover
    avg_cloud = weather_entry.get('avg_cloud_cover', 0)
    if avg_cloud > 75:
        state['cloud_cover'] = 'Overcast'
    elif avg_cloud > 50:
        state['cloud_cover'] = 'Partly Cloudy'

    # Wind
    wind_speed = weather_entry.get('wind_speed_m_s', 0)
    if wind_speed > 30:
        state['wind'] = 'Storm'
    elif wind_speed > 15:
        state['wind'] = 'Windy'

    # Flood Risk
    flood_status = weather_entry.get('flood', 'No Flood')  # Default to 'No Flood' if 'flood' key is missing
    if flood_status == 'Flood':
        state['flood'] = 'Flood'
    else:
        state['flood'] = 'No Flood'

    return state
