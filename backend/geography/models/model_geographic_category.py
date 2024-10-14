from django.db import models
from parler.models import TranslatableModel, TranslatedFields

class GeographicCategory(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255)  # Name field that can be translated
    )
    slug = models.SlugField(max_length=255, unique=True)  # Unique slug for the category

    def __str__(self):
        name = self.safe_translation_getter('name', any_language=True)
        return name or 'Unnamed Category'  # Fallback if name is not set

    class Meta:
        verbose_name_plural = "Geographic Categories"  # Plural name for admin interface
