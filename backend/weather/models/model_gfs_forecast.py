from django.contrib.gis.db import models
from geography.models import GeographicPlace

class GFSForecast(models.Model):
    place = models.ForeignKey(
        GeographicPlace,
        on_delete=models.CASCADE,
        related_name='gfs_forecasts'
    )
    date = models.DateField()
    hour = models.PositiveSmallIntegerField()
    utc_cycle_time = models.CharField(
        max_length=2,
        choices=[('00', '00'), ('06', '06'), ('12', '12'), ('18', '18')]
    )
    forecast_data = models.JSONField()

    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.PointField(null=True, blank=True)  # Make the field nullable

    class Meta:
        unique_together = ('place', 'date', 'hour', 'utc_cycle_time')
        indexes = [
            models.Index(fields=['date', 'hour']),
            models.Index(fields=['place', 'date']),
            models.Index(fields=['utc_cycle_time']),
        ]
        ordering = ['date', 'hour', 'utc_cycle_time']

    def __str__(self):
        return f"Forecast for {self.place.name} on {self.date} at {self.hour}:00 UTC"
