import os
from django.core.exceptions import ImproperlyConfigured

environment = os.getenv('DJANGO_ENVIRONMENT', 'development').lower()

if environment == 'production':
    from .production import *
elif environment == 'development':
    from .development import *
else:
    raise ImproperlyConfigured(f"Invalid DJANGO_ENVIRONMENT: {environment}")
