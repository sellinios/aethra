from django.db import models
from parler.models import TranslatableModel, TranslatedFields

class GeographicPlanet(TranslatableModel):  # Inherit from TranslatableModel
    translations = TranslatedFields(
        name=models.CharField(max_length=100, unique=True),
    )

    # Non-translatable fields
    mass = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    radius = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    distance_from_sun = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    orbital_period = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gravity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    has_life = models.BooleanField(default=False)
    is_exoplanet = models.BooleanField(default=False)
    star_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

    class Meta:
        verbose_name = "Geographic Planet"
        verbose_name_plural = "Geographic Planets"
