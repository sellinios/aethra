from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView  # For React frontend catch-all

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface
]

# Language-prefixed API URL patterns
urlpatterns += i18n_patterns(
    path('api/', include('api.urls')),  # Include the API URLs under the language prefix
)