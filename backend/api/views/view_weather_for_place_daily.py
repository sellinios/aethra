from django.http import JsonResponse
from django.utils.translation import get_language
from django.utils import timezone
from geography.models import GeographicPlace
from weather.models import GFSForecast
from api.serializers import DailyWeatherSerializer
from django.db.models import Max, Min, Avg, FloatField
from django.db.models.functions import TruncDate, Cast
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

    # Get today's date in the specified timezone
    today = timezone.now().date()
    logger.debug(f"Today's date: {today}")

    # Fetch and aggregate daily weather data from GFSForecast
    daily_forecasts = (
        GFSForecast.objects.filter(place=place, date__gte=today)  # Removed '__date' lookup
        .annotate(date_only=TruncDate('date'))
        .values('date_only')
        .annotate(
            max_temp=Max(Cast('forecast_data__2t_level_2_heightAboveGround', FloatField())),
            min_temp=Min(Cast('forecast_data__2t_level_2_heightAboveGround', FloatField())),
            avg_cloud_cover=Avg(Cast('forecast_data__lcc_level_0_lowCloudLayer', FloatField())),
            max_precipitation=Max(Cast('forecast_data__tp_level_0_surface', FloatField())),
            wind_speed_avg=Avg(Cast('forecast_data__10u_level_10_heightAboveGround', FloatField())),
        )
        .order_by('date_only')
    )

    logger.debug(f"Number of daily forecasts fetched: {daily_forecasts.count()}")

    # Reconstruct the date from the extracted date_only
    daily_weather_data = [
        {
            'date': forecast['date_only'].strftime('%Y-%m-%d') if forecast.get('date_only') else None,
            'max_temp': (forecast['max_temp'] - 273.15) if forecast.get('max_temp') is not None else None,
            'min_temp': (forecast['min_temp'] - 273.15) if forecast.get('min_temp') is not None else None,
            'avg_cloud_cover': forecast.get('avg_cloud_cover'),
            'max_precipitation': forecast.get('max_precipitation'),
            'wind_speed_avg': forecast.get('wind_speed_avg'),
        }
        for forecast in daily_forecasts
    ]

    logger.debug(f"Processed daily weather data: {daily_weather_data}")

    # Serialize the data
    serializer = DailyWeatherSerializer(daily_weather_data, many=True)

    response_data = {
        'place_name': place.safe_translation_getter('name', language_code=language, any_language=True),
        'daily_weather_data': serializer.data,
    }

    logger.debug(f"Response data: {response_data}")

    return JsonResponse(response_data)
