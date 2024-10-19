from django.http import JsonResponse
from django.utils.translation import get_language
from django.utils import timezone
from geography.models import GeographicPlace
from weather.models import GFSForecast
from api.serializers import DailyWeatherSerializer
from django.db.models import Max, Min, Avg
from django.db.models.functions import TruncDate
from django.db.models import FloatField, Cast

def weather_for_place_daily(request, place_slug):
    language = get_language()

    # Find the place
    try:
        place = GeographicPlace.objects.get(slug=place_slug)
    except GeographicPlace.DoesNotExist:
        return JsonResponse({'error': 'Place not found.'}, status=404)

    # Get today's date in the specified timezone
    today = timezone.now().date()

    # Fetch and aggregate daily weather data from GFSForecast
    daily_forecasts = (
        GFSForecast.objects.filter(place=place, date__gte=today)  # Filter out past dates
        .annotate(date_only=TruncDate('date'))  # Truncate datetime to date
        .values('date_only')  # Group by date
        .annotate(
            max_temp=Max(Cast('forecast_data__2t_level_2_heightAboveGround', FloatField())),  # Cast to Float
            min_temp=Min(Cast('forecast_data__2t_level_2_heightAboveGround', FloatField())),
            avg_cloud_cover=Avg(Cast('forecast_data__lcc_level_0_lowCloudLayer', FloatField())),
            max_precipitation=Max(Cast('forecast_data__tp_level_0_surface', FloatField())),
            wind_speed_avg=Avg(Cast('forecast_data__10u_level_10_heightAboveGround', FloatField())),
        )
        .order_by('date_only')  # Sort by date ascending
    )

    # Reconstruct the date from the extracted date_only
    daily_weather_data = [
        {
            'date': forecast['date_only'].strftime('%Y-%m-%d'),
            'max_temp': forecast['max_temp'] - 273.15,  # Convert from Kelvin to Celsius
            'min_temp': forecast['min_temp'] - 273.15,  # Convert from Kelvin to Celsius
            'avg_cloud_cover': forecast['avg_cloud_cover'],
            'max_precipitation': forecast['max_precipitation'],
            'wind_speed_avg': forecast['wind_speed_avg'],
        }
        for forecast in daily_forecasts
    ]

    # Serialize the data
    serializer = DailyWeatherSerializer(daily_weather_data, many=True)

    response_data = {
        'place_name': place.safe_translation_getter('name', language_code=language, any_language=True),
        'daily_weather_data': serializer.data,
    }

    return JsonResponse(response_data)
