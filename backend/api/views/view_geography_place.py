# api/views/view_geography_place.py

from django.http import JsonResponse
from django.utils.translation import get_language
from geography.models import GeographicPlace, GeographicDivision

def place_detail(request, country_slug, region_slug, municipality_slug, place_slug):
    language = get_language()

    # Get the municipality
    try:
        municipality = GeographicDivision.objects.get(
            slug=municipality_slug
        )
    except GeographicDivision.DoesNotExist:
        return JsonResponse({'error': 'Municipality not found.'}, status=404)

    # Find the place
    try:
        place = GeographicPlace.objects.get(
            slug=place_slug,
            admin_division=municipality
        )
    except GeographicPlace.DoesNotExist:
        return JsonResponse({'error': 'Place not found.'}, status=404)

    # Prepare response data
    response_data = {
        'name': place.safe_translation_getter('name', language_code=language, any_language=True),
        'description': place.safe_translation_getter('description', language_code=language, any_language=True),
        'latitude': place.latitude,
        'longitude': place.longitude,
        'elevation': place.elevation,
        'municipality_name': municipality.safe_translation_getter('name', language_code=language, any_language=True),
        'municipality_slug': municipality.slug,
        # Include other necessary fields or slugs if needed
    }

    return JsonResponse(response_data)
