# api/views/view_weather_for_place.py

from django.http import JsonResponse
from django.utils.translation import get_language
from geography.models import GeographicPlace
from api.utils import get_weather_data_for_place

def weather_for_place(request, place_slug):
    language = get_language()

    # Find the place
    try:
        place = GeographicPlace.objects.get(slug=place_slug)
    except GeographicPlace.DoesNotExist:
        return JsonResponse({'error': 'Place not found.'}, status=404)

    # Fetch weather data
    weather_data = get_weather_data_for_place(place)

    response_data = {
        'place_name': place.safe_translation_getter('name', language_code=language, any_language=True),
        'weather_data': weather_data,
    }

    return JsonResponse(response_data)
