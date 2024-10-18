# api/views/view_geography_nearest_place.py
import logging
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.utils.translation import get_language
from geography.models import GeographicPlace

def nearest_place(request):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    language = get_language()

    # Ensure language is a string
    if not language:
        language = 'en'  # Default language code
    else:
        # If language is a list, take the first element
        if isinstance(language, list):
            language = language[0]
        # Ensure language is a string
        language = str(language)
        # Normalize the language code (e.g., 'el' from 'el-gr')
        language = language.split('-')[0]

    logging.warning(f"Final 'language' value: {language}, type: {type(language)}")

    if not latitude or not longitude:
        return JsonResponse({'error': 'Latitude and longitude are required.'}, status=400)

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid latitude or longitude.'}, status=400)

    user_location = Point(longitude, latitude, srid=4326)

    # Find the nearest place
    place = GeographicPlace.objects.annotate(
        distance=Distance('location', user_location)
    ).order_by('distance').first()

    if not place:
        return JsonResponse({'error': 'No places found.'}, status=404)

    response_data = {
        'name': place.safe_translation_getter('name', language_code=language, any_language=True),
        'description': place.safe_translation_getter('description', language_code=language, any_language=True),
        'latitude': place.latitude,
        'longitude': place.longitude,
        'elevation': place.elevation,
        'continent_slug': place.get_continent_slug(),
        'country_slug': place.get_country_slug(),
        'region_slug': place.get_region_slug(),
        'municipality_slug': place.admin_division.slug,
        'municipality_name': place.admin_division.safe_translation_getter('name', language_code=language, any_language=True),
        'place_slug': place.slug,
    }

    return JsonResponse(response_data)
