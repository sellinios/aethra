from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import GeographicPlanet, GeographicPlace, GeographicDivision, GeographicCategory

@admin.register(GeographicPlanet)
class GeographicPlanetAdmin(TranslatableAdmin):  # Use TranslatableAdmin for translations
    list_display = ('get_name', 'mass', 'radius', 'distance_from_sun', 'orbital_period', 'gravity', 'has_life', 'is_exoplanet', 'star_name')
    search_fields = ('translations__name', 'star_name')  # Search within translations
    list_filter = ('is_exoplanet', 'has_life', 'star_name')
    list_editable = ('mass', 'radius', 'distance_from_sun', 'orbital_period', 'gravity', 'has_life', 'is_exoplanet')
    ordering = ('translations__name',)  # Order by translated name
    list_per_page = 20

    # Helper method to get translated name
    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True) or "Unnamed Planet"
    get_name.short_description = 'Name'

@admin.register(GeographicPlace)
class GeographicPlaceAdmin(TranslatableAdmin):  # Use TranslatableAdmin for translated fields
    list_display = ('get_name', 'longitude', 'latitude', 'confirmed', 'category', 'admin_division')
    search_fields = ('translations__name',)  # Use translations__name for searching translated fields
    list_filter = ('confirmed', 'category', 'admin_division')
    ordering = ('id', 'translations__name')  # Make sure 'id' comes first to match the distinct query
    list_per_page = 20

    def get_queryset(self, request):
        # Ensure the queryset uses distinct by 'id' while ordering by 'id' first, followed by 'translations__name'
        qs = super().get_queryset(request)
        return qs.order_by('id', 'translations__name').distinct('id')

    # Helper method to get translated name
    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True) or "Unnamed Place"
    get_name.short_description = 'Name'

@admin.register(GeographicDivision)
class GeographicDivisionAdmin(TranslatableAdmin):  # Use TranslatableAdmin for translations
    list_display = ('get_name', 'get_level_name', 'parent', 'confirmed')
    search_fields = ('translations__name', 'translations__level_name')
    list_filter = ('confirmed', 'parent')
    ordering = ('translations__name',)
    list_per_page = 20

    # Helper method to get translated name
    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True) or "Unnamed Division"
    get_name.short_description = 'Name'

    # Helper method to get translated level name
    def get_level_name(self, obj):
        return obj.safe_translation_getter('level_name', any_language=True) or "Unnamed Level"
    get_level_name.short_description = 'Level Name'

@admin.register(GeographicCategory)
class GeographicCategoryAdmin(TranslatableAdmin):
    list_display = ('get_name', 'slug')
    search_fields = ('translations__name',)
    ordering = ('slug',)
    list_per_page = 20

    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True) or "Unnamed Category"
    get_name.short_description = 'Name'