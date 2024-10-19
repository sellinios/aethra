# geography/admin.py

from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import GeographicPlanet, GeographicPlace, GeographicDivision, GeographicCategory
from .forms import GeographicPlaceForm  # Import the custom form

@admin.register(GeographicPlanet)
class GeographicPlanetAdmin(TranslatableAdmin):
    list_display = ('get_name', 'mass', 'radius', 'distance_from_sun', 'orbital_period', 'gravity', 'has_life', 'is_exoplanet', 'star_name')
    search_fields = ('translations__name', 'star_name')
    list_filter = ('is_exoplanet', 'has_life', 'star_name')
    list_editable = ('mass', 'radius', 'distance_from_sun', 'orbital_period', 'gravity', 'has_life', 'is_exoplanet')
    ordering = ('translations__name',)
    list_per_page = 20

    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True) or "Unnamed Planet"
    get_name.short_description = 'Name'


@admin.register(GeographicPlace)
class GeographicPlaceAdmin(TranslatableAdmin):
    form = GeographicPlaceForm  # Use the custom form
    list_display = ('get_name', 'longitude', 'latitude', 'confirmed', 'category', 'admin_division')
    search_fields = ('translations__name',)
    list_filter = ('confirmed', 'category', 'admin_division')
    ordering = ('id', 'translations__name')
    list_per_page = 20
    change_list_template = "admin/geography/geographicplace/change_list.html"  # Custom change list template

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('id', 'translations__name').distinct('id')

    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True) or "Unnamed Place"
    get_name.short_description = 'Name'

    # Add custom admin URLs
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('map/', self.admin_site.admin_view(self.map_view), name='geographicplace_map'),
        ]
        return custom_urls + urls

    # Custom map view
    def map_view(self, request):
        from django.shortcuts import render
        places = GeographicPlace.objects.filter(latitude__isnull=False, longitude__isnull=False)
        places_data = [
            {
                'name': place.safe_translation_getter('name', any_language=True) or "Unnamed Place",
                'latitude': place.latitude,
                'longitude': place.longitude,
                'admin_division': place.admin_division.safe_translation_getter('name', any_language=True) if place.admin_division else "N/A",
            }
            for place in places
        ]
        context = dict(
            self.admin_site.each_context(request),
            places=places_data,
        )
        return render(request, 'admin/geography/geographicplace/map_view.html', context)


@admin.register(GeographicDivision)
class GeographicDivisionAdmin(TranslatableAdmin):
    list_display = ('get_name', 'get_level_name', 'parent', 'confirmed', 'boundary_info')
    search_fields = ('translations__name', 'translations__level_name')
    list_filter = ('confirmed', 'parent')
    ordering = ('translations__name',)
    list_per_page = 20

    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True) or "Unnamed Division"
    get_name.short_description = 'Name'

    def get_level_name(self, obj):
        return obj.safe_translation_getter('level_name', any_language=True) or "Unnamed Level"
    get_level_name.short_description = 'Level Name'

    def boundary_info(self, obj):
        if obj.boundary:
            return f"Boundary Area: {obj.boundary.area:.2f} sq.km"
        return "No Boundary"
    boundary_info.short_description = 'Boundary Info'


@admin.register(GeographicCategory)
class GeographicCategoryAdmin(TranslatableAdmin):
    list_display = ('get_name', 'slug')
    search_fields = ('translations__name',)
    ordering = ('slug',)
    list_per_page = 20

    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True) or "Unnamed Category"
    get_name.short_description = 'Name'
