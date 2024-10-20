import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
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
    'parler',  # Parler for multilingual support
    'corsheaders',  # CORS headers support
    'rest_framework',  # Django REST framework for APIs
    'django.contrib.gis',  # GeoDjango GIS features
    'leaflet',

    # Your Django apps
    'api',  # Adjust according to your actual app name
    'geography',
    'weather',
    'weather_engine',
    'tinymce',
    'articles',
    'eshop',  # The e-commerce app
    'erp',  # The ERP app
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Allow CORS for your APIs
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # LocaleMiddleware for language detection
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
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
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
LANGUAGE_CODE = 'en'  # Set your default language (e.g., 'en')

# Supported languages
LANGUAGES = [
    ('en', 'English'),
    ('el', 'Greek'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('de', 'German'),
    ('it', 'Italian'),
    ('ru', 'Russian'),
    ('zh-hans', 'Simplified Chinese'),
    ('ja', 'Japanese'),
    ('pt', 'Portuguese'),
]

USE_TZ = True
TIME_ZONE = 'Europe/Athens'

USE_I18N = True
USE_L10N = True

# Paths to translation files (usually .po and .mo files for different languages)
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# ------------------------------
# STATIC AND MEDIA FILES
# ------------------------------
STATIC_URL = '/django_static/'

# Multiple static directories for kairos and fthina
STATICFILES_DIRS = [
    BASE_DIR / 'static/kairos',  # Static files for kairos site
    BASE_DIR / 'static/fthina',  # Static files for fthina site
]

# Where collectstatic will gather the static files in production
STATIC_ROOT = BASE_DIR / 'staticfiles'

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
    None: [
        {'code': 'en', 'name': 'English'},
        {'code': 'el', 'name': 'Greek'},
        {'code': 'es', 'name': 'Spanish'},
        {'code': 'fr', 'name': 'French'},
        {'code': 'de', 'name': 'German'},
        {'code': 'it', 'name': 'Italian'},
        {'code': 'ru', 'name': 'Russian'},
        {'code': 'zh-hans', 'name': 'Simplified Chinese'},
        {'code': 'ja', 'name': 'Japanese'},
        {'code': 'pt', 'name': 'Portuguese'},
    ],
    'default': {
        'fallback': 'en',  # Fallback to English (should be a string, not a list)
        'hide_untranslated': False,
    }
}

# ------------------------------
# CORS HEADERS SETTINGS
# ------------------------------
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv('DJANGO_CORS_ALLOWED_ORIGINS', '').split(',')
    if origin.strip()
]

# Add these lines for TinyMCE configuration
TINYMCE_DEFAULT_CONFIG = {
    'height': '500px',
    'width': '100%',
    'menubar': 'file edit view insert format tools table help',
    'plugins': '''
        preview paste searchreplace autolink directionality code visualblocks
        visualchars fullscreen image link media template codesample table charmap hr
        pagebreak nonbreaking anchor insertdatetime advlist lists wordcount textpattern
        help
    ''',
    'toolbar': '''
        undo redo | bold italic underline strikethrough | fontselect fontsizeselect
        formatselect | alignleft aligncenter alignright alignjustify | outdent indent |
        numlist bullist | forecolor backcolor removeformat | pagebreak | charmap emoticons |
        fullscreen preview save print | insertfile image media template link anchor codesample |
        ltr rtl
    ''',
    'images_upload_url': '/tinymce/upload/',
    'images_upload_credentials': True,
    'content_css': '/static/css/content.css',  # Optional: Use custom CSS
    'custom_undo_redo_levels': 20,
    'entity_encoding': 'raw',  # Add this line
}
