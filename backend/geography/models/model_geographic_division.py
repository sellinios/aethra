from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from parler.models import TranslatableModel, TranslatedFields

class GeographicDivision(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255),
        level_name=models.CharField(max_length=255),
        name_variations=ArrayField(models.CharField(max_length=255), default=list, blank=True),
    )

    slug = models.SlugField(max_length=255, unique=True, blank=True)  # Non-translated slug
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    geographic_data = models.ForeignKey('GeographicData', null=True, blank=True, on_delete=models.SET_NULL,
                                        related_name='divisions')
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            name = self.safe_translation_getter('name', any_language=True)
            self.slug = slugify(name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Geographic Divisions"
