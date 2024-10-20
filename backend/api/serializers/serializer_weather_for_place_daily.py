# api/serializers/serializer_weather_for_place_daily.py

from rest_framework import serializers

class DailyWeatherSerializer(serializers.Serializer):
    date = serializers.DateField()
    max_temp = serializers.FloatField()
    min_temp = serializers.FloatField()
    avg_cloud_cover = serializers.FloatField()
    max_precipitation = serializers.FloatField()
    wind_speed_avg = serializers.FloatField()

    class Meta:
        fields = ['date', 'max_temp', 'min_temp', 'avg_cloud_cover', 'max_precipitation', 'wind_speed_avg']

class AlertSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField()
    level = serializers.CharField(max_length=10)
