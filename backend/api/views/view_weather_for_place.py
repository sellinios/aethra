# api/views/view_weather_for_place.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.translation import get_language
from geography.models import GeographicPlace
from api.utils.weather_data import get_weather_data_for_place
from api.utils.weather_state import determine_weather_state
from api.utils.alerts import generate_alerts_for_weather
from api.serializers import AlertSerializer, DailyWeatherSerializer  # Correct import
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def weather_for_place(request, place_slug):
    language = get_language()

    # Find the place
    try:
        place = GeographicPlace.objects.get(slug=place_slug)
    except GeographicPlace.DoesNotExist:
        return Response({'error': 'Place not found.'}, status=404)

    # Fetch weather data
    weather_data = get_weather_data_for_place(place)

    # Generate alerts based on the latest weather entry
    alerts = []
    if weather_data:
        latest_weather = weather_data[-1]  # Assuming latest is last
        alerts = generate_alerts_for_weather(place, latest_weather)

    # Determine weather state for the latest forecast
    if weather_data:
        latest_weather = weather_data[-1]
        weather_state = determine_weather_state(latest_weather)
    else:
        weather_state = {}

    # Serialize alerts
    serializer = AlertSerializer(alerts, many=True)

    response_data = {
        'place_name': place.safe_translation_getter('name', language_code=language, any_language=True),
        'weather_data': weather_data,
        'weather_state': weather_state,
        'alerts': serializer.data,  # Include the serialized alerts
    }

    return Response(response_data)
