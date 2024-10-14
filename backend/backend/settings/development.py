# backend/backend/settings/development.py

from .base import *

# ------------------------------
# SECURITY SETTINGS
# ------------------------------
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ['true', '1', 't']

ALLOWED_HOSTS = [host.strip() for host in os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')]

# ------------------------------
# DATABASE CONFIGURATION
# ------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': get_env_variable('POSTGRES_DB'),
        'USER': get_env_variable('POSTGRES_USER'),
        'PASSWORD': get_env_variable('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

# ------------------------------
# EMAIL CONFIGURATION
# ------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ------------------------------
# SECURITY ENHANCEMENTS
# ------------------------------
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# ------------------------------
# OTHER DEVELOPMENT SETTINGS
# ------------------------------
# Add any other development-specific settings below

# ------------------------------
# CORS SETTINGS
# ------------------------------
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

# Uncomment this for development purposes to allow all origins:
# CORS_ALLOW_ALL_ORIGINS = True
