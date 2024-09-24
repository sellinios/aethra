import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Function to get environment variables with validation
def get_env_variable(var_name):
    value = os.getenv(var_name)
    if value is None:
        raise ImproperlyConfigured(f"The {var_name} environment variable is not set.")
    return value


# ------------------------------
# SECURITY SETTINGS
# ------------------------------
SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')

DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ['true', '1', 't']

ALLOWED_HOSTS = [host.strip() for host in os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')]

# ------------------------------
# APPLICATION DEFINITION
# ------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'parler',
    'corsheaders',
    'rest_framework',

    # Your Django apps
    'api',  # Replace 'api' with your actual app name
    'geography',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this line
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# ------------------------------
# DATABASE CONFIGURATION
# ------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable('POSTGRES_DB'),
        'USER': get_env_variable('POSTGRES_USER'),
        'PASSWORD': get_env_variable('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

# ------------------------------
# PASSWORD VALIDATION
# ------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ------------------------------
# INTERNATIONALIZATION
# ------------------------------
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# ------------------------------
# STATIC AND MEDIA FILES
# ------------------------------
STATIC_URL = '/django_static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------------
# SECURITY ENHANCEMENTS
# ------------------------------
SECURE_SSL_REDIRECT = False  # To be overridden in production
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# ------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------
# EMAIL CONFIGURATION
# ------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env_variable('DJANGO_EMAIL_HOST')
EMAIL_PORT = int(os.getenv('DJANGO_EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('DJANGO_EMAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
EMAIL_HOST_USER = get_env_variable('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('DJANGO_EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = get_env_variable('DJANGO_DEFAULT_FROM_EMAIL')

# ------------------------------
# CSRF SETTINGS
# ------------------------------
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin.strip()
]

# ------------------------------
# PARLER LANGUAGE SETTINGS
# ------------------------------
PARLER_LANGUAGES = {
    None: (
        {'code': 'en', 'name': 'English'},
        {'code': 'fr', 'name': 'French'},  # Add more languages as needed
    ),
    'default': {
        'fallbacks': ['en'],  # Fallback to English if translation not available
        'hide_untranslated': False,  # Show untranslated content instead of hiding it
    }
}
