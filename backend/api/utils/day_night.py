# api/utils/day_night.py

from astral import LocationInfo
from astral.sun import sun
from django.utils import timezone
import pytz


def is_daytime(forecast_datetime, latitude, longitude):
    """
    Determines if the given datetime is during day or night for the specified location.

    Parameters:
    - forecast_datetime (datetime): The datetime to check.
    - latitude (float): Latitude of the location.
    - longitude (float): Longitude of the location.

    Returns:
    - str: 'day' or 'night'
    """
    try:
        # Determine the timezone based on latitude and longitude
        # For simplicity, assuming UTC; for accurate results, use a timezone lookup library like timezonefinder
        timezone_str = 'UTC'
        tz = pytz.timezone(timezone_str)
        forecast_datetime = forecast_datetime.astimezone(tz)

        location = LocationInfo(name="Custom Location", region="Custom Region", timezone=timezone_str,
                                latitude=latitude, longitude=longitude)
        s = sun(location.observer, date=forecast_datetime.date(), tzinfo=tz)
        sunrise = s['sunrise']
        sunset = s['sunset']

        if sunrise <= forecast_datetime <= sunset:
            return 'day'
        else:
            return 'night'
    except Exception as e:
        # In case of any error, default to day
        return 'day'
