import logging

logger = logging.getLogger(__name__)

def categorize_precipitation(weather_entry):
    """
    Categorize precipitation based on total precipitation, convective precipitation rate, and temperature.

    Parameters:
    - weather_entry (dict): A dictionary containing precipitation and temperature parameters.

    Returns:
    - str: A string representing the precipitation category.
    """
    # Fetch parameters from weather_entry
    total_precipitation = weather_entry.get('total_precipitation_mm')
    convective_precipitation_rate = weather_entry.get('convective_precipitation_rate_mm_h')
    temperature_celsius = weather_entry.get('temperature_celsius')  # 2-meter temperature
    precipitation_type = weather_entry.get('precipitation_type')

    # Log the parameters for debugging
    logger.debug(f"total_precipitation: {total_precipitation}")
    logger.debug(f"convective_precipitation_rate: {convective_precipitation_rate}")
    logger.debug(f"temperature_celsius: {temperature_celsius}")

    # Ensure that the required parameters exist
    if total_precipitation is None:
        logger.warning("Total precipitation data is missing.")
        return 'Data Unavailable'

    if temperature_celsius is None:
        logger.warning("Temperature data is missing.")
        return 'Data Unavailable'

    # Define thresholds for categorization
    SEVERE_STORM_THRESHOLD = 50
    MODERATE_STORM_THRESHOLD = 20
    LIGHT_STORM_THRESHOLD = 10

    EXTREME_RAIN_THRESHOLD = 100
    HEAVY_RAIN_THRESHOLD = 50
    MODERATE_RAIN_THRESHOLD = 25
    LIGHT_RAIN_THRESHOLD = 5

    SNOW_TEMPERATURE_THRESHOLD = 3  # degrees Celsius

    # Categorize convective precipitation
    if convective_precipitation_rate is not None:
        if convective_precipitation_rate > SEVERE_STORM_THRESHOLD:
            return 'Severe Storm'
        elif convective_precipitation_rate > MODERATE_STORM_THRESHOLD:
            return 'Moderate Storm'
        elif convective_precipitation_rate > LIGHT_STORM_THRESHOLD:
            return 'Light Storm'

    # Categorize precipitation based on type and total precipitation
    if precipitation_type == 'snow':
        if temperature_celsius < SNOW_TEMPERATURE_THRESHOLD:
            if total_precipitation > 50:
                return 'Heavy Snow'
            elif total_precipitation > 25:
                return 'Moderate Snow'
            else:
                return 'Light Snow'
        else:
            logger.warning(f"Temperature is {temperature_celsius}°C but precipitation type is snow.")
            return 'No Precipitation'

    elif precipitation_type == 'rain':
        if total_precipitation > EXTREME_RAIN_THRESHOLD:
            return 'Extreme Rain'
        elif total_precipitation > HEAVY_RAIN_THRESHOLD:
            return 'Heavy Rain'
        elif total_precipitation > MODERATE_RAIN_THRESHOLD:
            return 'Moderate Rain'
        elif total_precipitation > LIGHT_RAIN_THRESHOLD:
            return 'Light Rain'
        elif total_precipitation > 0:
            return 'Drizzle'
        else:
            return 'No Precipitation'

    elif precipitation_type == 'sleet':
        return 'Sleet'

    else:
        logger.warning(f"Unknown precipitation type: {precipitation_type}")
        return 'Unknown Precipitation Type'
