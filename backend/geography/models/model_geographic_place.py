# geography/models/model_geographic_place.py

from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields
from unidecode import unidecode

class GeographicPlace(TranslatableModel):
    id = models.AutoField(primary_key=True)
    translations = TranslatedFields(
        name=models.CharField(max_length=255, null=True, blank=True),
        slug=models.SlugField(max_length=255, blank=True),
        description=models.TextField(null=True, blank=True),
    )
    longitude = models.FloatField()
    latitude = models.FloatField()
    elevation = models.FloatField(null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    category = models.ForeignKey('GeographicCategory', on_delete=models.SET_DEFAULT, default=1)
    admin_division = models.ForeignKey('GeographicDivision', on_delete=models.CASCADE, related_name='places')
    location = gis_models.PointField(geography=True, null=True, blank=True)

    class Meta:
        verbose_name = "Geographic Place"
        verbose_name_plural = "Geographic Places"
        indexes = [
            models.Index(fields=['longitude', 'latitude']),
        ]

    def __str__(self):
        name = self.safe_translation_getter('name', any_language=True)
        return f"{name or 'Unnamed Place'} ({self.latitude}, {self.longitude})"

    def clean(self):
        if not self.admin_division:
            raise ValidationError('Place must be associated with a GeographicDivision.')

        # Validate latitude and longitude
        if not (-90 <= self.latitude <= 90):
            raise ValidationError('Latitude must be between -90 and 90 degrees.')
        if not (-180 <= self.longitude <= 180):
            raise ValidationError('Longitude must be between -180 and 180 degrees.')

        # Ensure no more than six decimal places
        self.latitude = round(self.latitude, 6)
        self.longitude = round(self.longitude, 6)

    def save(self, *args, **kwargs):
        self.clean()
        self.location = Point(self.longitude, self.latitude, srid=4326)
        if self.elevation is None:
            self.elevation = 0

        # Save first to get an ID if it's a new object
        if not self.id:
            super().save(*args, **kwargs)

        # Ensure language handling is correct
        for lang in self.get_available_languages():
            self.set_current_language(lang)
            if not self.safe_translation_getter('name'):
                self.name = "To Be Defined"

            # Generate the base slug
            name = self.safe_translation_getter('name')
            base_slug = slugify(unidecode(name))

            # Include language code and ID in the slug to ensure uniqueness
            unique_slug = f"{base_slug}-{lang}-{self.id}"

            # Assign the slug
            self.slug = unique_slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('place_detail', kwargs={
            'continent_slug': self.get_continent_slug(),
            'country_slug': self.get_country_slug(),
            'region_slug': self.get_region_slug(),
            'municipality_slug': self.admin_division.safe_translation_getter('slug'),
            'place_slug': self.safe_translation_getter('slug'),
        })

    # Helper methods to get slugs
    def get_continent_slug(self, language=None):
        division = self.admin_division
        while division.parent is not None:
            division = division.parent
        return division.safe_translation_getter('slug', language_code=language, any_language=True)

    def get_country_slug(self, language=None):
        division = self.admin_division
        while division.parent is not None:
            if division.parent.parent is None:
                return division.safe_translation_getter('slug', language_code=language, any_language=True)
            division = division.parent
        return division.safe_translation_getter('slug', language_code=language, any_language=True)

    def get_region_slug(self, language=None):
        division = self.admin_division
        while division.parent is not None:
            if division.parent.parent is not None and division.parent.parent.parent is None:
                return division.safe_translation_getter('slug', language_code=language, any_language=True)
            division = division.parent
        return division.safe_translation_getter('slug', language_code=language, any_language=True)
