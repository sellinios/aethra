from django.http import JsonResponse
from django.utils.translation import get_language
from geography.models import GeographicPlace
from weather.models import GFSForecast
from api.serializers import DailyWeatherSerializer
from django.db.models import Max, Min, Avg
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay, Cast
from django.db.models import FloatField

def weather_for_place_daily(request, place_slug):
    language = get_language()

    # Find the place
    try:
        place = GeographicPlace.objects.get(slug=place_slug)
    except GeographicPlace.DoesNotExist:
        return JsonResponse({'error': 'Place not found.'}, status=404)

    # Fetch and aggregate daily weather data from GFSForecast using ExtractYear, ExtractMonth, and ExtractDay
    daily_forecasts = (
        GFSForecast.objects.filter(place=place)
        .annotate(
            year=ExtractYear('date'),
            month=ExtractMonth('date'),
            day=ExtractDay('date')
        )
        .values('year', 'month', 'day')
        .annotate(
            max_temp=Max(Cast('forecast_data__2t_level_2_heightAboveGround', FloatField())),  # Cast to Float
            min_temp=Min(Cast('forecast_data__2t_level_2_heightAboveGround', FloatField())),
            avg_cloud_cover=Avg(Cast('forecast_data__lcc_level_0_lowCloudLayer', FloatField())),
            max_precipitation=Max(Cast('forecast_data__tp_level_0_surface', FloatField())),
            wind_speed_avg=Avg(Cast('forecast_data__10u_level_10_heightAboveGround', FloatField())),
        )
        .order_by('year', 'month', 'day')
    )

    # Reconstruct the date from the extracted year, month, and day
    daily_weather_data = [
        {
            'date': f"{forecast['year']}-{forecast['month']:02d}-{forecast['day']:02d}",
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