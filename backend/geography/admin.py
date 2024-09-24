from django.contrib import admin
from .models import GeographicPlanet, GeographicPlace, GeographicDivision, GeographicCategory

@admin.register(GeographicPlanet)
class GeographicPlanetAdmin(admin.ModelAdmin):
    list_display = ('name', 'mass', 'radius', 'distance_from_sun', 'orbital_period', 'gravity', 'has_life', 'is_exoplanet', 'star_name')
    search_fields = ('name', 'star_name')
    list_filter = ('is_exoplanet', 'has_life', 'star_name')
    list_editable = ('mass', 'radius', 'distance_from_sun', 'orbital_period', 'gravity', 'has_life', 'is_exoplanet')
    ordering = ('name',)
    list_per_page = 20

@admin.register(GeographicPlace)
class GeographicPlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'longitude', 'latitude', 'confirmed', 'category', 'admin_division')
    search_fields = ('translations__name',)  # Use the correct reference for search
    list_filter = ('confirmed', 'category', 'admin_division')
    ordering = ('translations__name',)  # Correct reference for ordering
    list_per_page = 20

@admin.register(GeographicDivision)
class GeographicDivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'level_name', 'parent', 'confirmed')
    search_fields = ('name', 'level_name')
    list_filter = ('confirmed', 'parent')
    ordering = ('name',)
    list_per_page = 20


@admin.register(GeographicCategory)
class GeographicCategoryAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'slug')
    search_fields = ('translations__name',)
    ordering = ('slug',)
    list_per_page = 20

    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True) or "Unnamed Category"
    get_name.short_description = 'Name'


