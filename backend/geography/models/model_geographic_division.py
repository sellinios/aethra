from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from parler.models import TranslatableModel, TranslatedFields

class GeographicDivision(TranslatableModel):  # Inherit from TranslatableModel for translations
    # Translatable fields
    translations = TranslatedFields(
        name=models.CharField(max_length=255),  # Name is translatable
        level_name=models.CharField(max_length=255),  # Level name is translatable
        name_variations=ArrayField(models.CharField(max_length=255), default=list, blank=True),  # Translatable array of name variations
    )

    # Non-translatable fields
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    geographic_data = models.ForeignKey('GeographicData', null=True, blank=True, on_delete=models.SET_NULL,
                                        related_name='divisions')
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)  # Use translated name

    def save(self, *args, **kwargs):
        # Automatically generate slug from the translated name if not provided
        if not self.slug:
            self.slug = slugify(self.safe_translation_getter('name', any_language=True))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Geographic Divisions"

    class ParlerMeta:
        # Enforce uniqueness of the translated fields
        unique_together = [
            ('name', 'parent', 'level_name'),  # Ensure name, parent, and level_name are unique together in translations
        ]


class Municipality(GeographicDivision):  # Inherit from GeographicDivision
    population = models.IntegerField(null=True, blank=True)
    area = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.safe_translation_getter('name', any_language=True)} Municipality"