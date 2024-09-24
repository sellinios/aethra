"""
This module defines the GeographicPlanet model, which represents a planet and its attributes.
"""

from django.db import models

class GeographicPlanet(models.Model):
    """
    Represents a planet and its attributes.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  # Assuming planet names are unique
    mass = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)  # in kg
    radius = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # in kilometers
    distance_from_sun = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)  # in million km (if applicable)
    orbital_period = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # in Earth days
    gravity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # in m/s²
    atmosphere_composition = models.TextField(blank=True, null=True)  # e.g., "Nitrogen, Oxygen"
    has_life = models.BooleanField(default=False)  # True if life is known on the planet
    is_exoplanet = models.BooleanField(default=False)  # True if this is an exoplanet (outside the solar system)
    star_name = models.CharField(max_length=100, blank=True, null=True)  # The name of the star this exoplanet orbits

    class Meta:
        verbose_name = "Geographic Planet"
        verbose_name_plural = "Geographic Planets"

    def __str__(self):
        """
        Return a string representation of the GeographicPlanet instance.
        """
        return str(self.name)
