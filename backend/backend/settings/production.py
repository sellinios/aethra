from .base import *

# ------------------------------
# SECURITY SETTINGS
# ------------------------------
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ['true', '1', 't']

ALLOWED_HOSTS = [host.strip() for host in os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')]

if not ALLOWED_HOSTS:
    raise ValueError("DJANGO_ALLOWED_HOSTS environment variable must be set for production.")

# ------------------------------
# DATABASE CONFIGURATION
# ------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('POSTGRES_DB_PROD', ''),
        'USER': os.getenv('POSTGRES_USER_PROD', ''),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD_PROD', ''),
        'HOST': os.getenv('POSTGRES_HOST_PROD', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT_PROD', '5432'),
    }
}

# ------------------------------
# EMAIL CONFIGURATION
# ------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# ------------------------------
# SECURITY ENHANCEMENTS
# ------------------------------
SECURE_SSL_REDIRECT = os.getenv('DJANGO_SECURE_SSL_REDIRECT', 'True').lower() in ['true', '1', 't']
SESSION_COOKIE_SECURE = os.getenv('DJANGO_SESSION_COOKIE_SECURE', 'True').lower() in ['true', 't']
CSRF_COOKIE_SECURE = os.getenv('DJANGO_CSRF_COOKIE_SECURE', 'True').lower() in ['true', 't']

SECURE_HSTS_SECONDS = int(os.getenv('DJANGO_SECURE_HSTS_SECONDS', '31536000'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True').lower() in ['true', '1', 't']
SECURE_HSTS_PRELOAD = os.getenv('DJANGO_SECURE_HSTS_PRELOAD', 'True').lower() in ['true', '1', 't']

# ------------------------------
# CORS SETTINGS
# ------------------------------
CORS_ALLOWED_ORIGINS = [
    'https://www.kairos.gr',  # Your production frontend
    'https://kairos.gr',      # Alternate domain, if needed
]