# api/views/view_weather_for_place_daily.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.utils.translation import get_language
from geography.models import GeographicPlace
from api.utils.weather_data import get_daily_weather_data_for_place
from api.serializers import DailyWeatherSerializer
import logging

logger = logging.getLogger(__name__)

def weather_for_place_daily(request, place_slug):
    language = get_language()

    # Find the place
    try:
        place = GeographicPlace.objects.get(slug=place_slug)
    except GeographicPlace.DoesNotExist:
        logger.error(f"Place with slug '{place_slug}' not found.")
        return JsonResponse({'error': 'Place not found.'}, status=404)

    # Fetch daily weather data
    daily_weather_data = get_daily_weather_data_for_place(place)

    # Serialize the data
    serializer = DailyWeatherSerializer(daily_weather_data, many=True)

    response_data = {
        'place_name': place.safe_translation_getter('name', language_code=language, any_language=True),
        'daily_weather_data': serializer.data,
    }

    logger.debug(f"Response data: {response_data}")

    return JsonResponse(response_data)
