from django.contrib import admin
from .models import GeographicPlanet  # Import your model


@admin.register(GeographicPlanet)
class GeographicPlanetAdmin(admin.ModelAdmin):
    # Customize columns displayed in the admin list view
    list_display = (
        'name',
        'mass',
        'radius',
        'distance_from_sun',
        'orbital_period',
        'gravity',
        'has_life',
        'is_exoplanet',
        'star_name'
    )

    # Add a search bar to search planets by name or star name
    search_fields = ('name', 'star_name')

    # Add filters to filter by exoplanet status, life presence, and star name
    list_filter = ('is_exoplanet', 'has_life', 'star_name')

    # Option to edit specific fields directly in the list view (optional)
    list_editable = ('mass', 'radius', 'distance_from_sun', 'orbital_period', 'gravity', 'has_life', 'is_exoplanet')

    # Additional configurations to improve the admin interface
    ordering = ('name',)  # Order by planet name by default
    list_per_page = 20  # Limit the number of items displayed per page
