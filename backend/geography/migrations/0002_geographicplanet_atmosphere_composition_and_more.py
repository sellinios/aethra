# Generated by Django 5.1.1 on 2024-09-23 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='geographicplanet',
            name='atmosphere_composition',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='geographicplanet',
            name='distance_from_sun',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='geographicplanet',
            name='gravity',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='geographicplanet',
            name='has_life',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='geographicplanet',
            name='is_exoplanet',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='geographicplanet',
            name='orbital_period',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='geographicplanet',
            name='star_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]