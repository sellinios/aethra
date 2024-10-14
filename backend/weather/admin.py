from django.contrib import admin
from weather_engine.models import GFSParameter

@admin.register(GFSParameter)
class GFSParameterAdmin(admin.ModelAdmin):
    list_display = ('number', 'level_layer', 'parameter', 'forecast_valid', 'description', 'last_updated', 'enabled')
    list_filter = ('last_updated', 'enabled')
    search_fields = ('number', 'parameter', 'description')
    ordering = ('number',)
    fields = ('number', 'level_layer', 'parameter', 'forecast_valid', 'description', 'last_updated', 'enabled')
    readonly_fields = ('last_updated',)

    actions = ['disable_parameters']

    def disable_parameters(self, request, queryset):
        updated_count = queryset.update(enabled=False)
        self.message_user(request, f"{updated_count} parameters have been disabled.")
    disable_parameters.short_description = "Disable selected parameters"