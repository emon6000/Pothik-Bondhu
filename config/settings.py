# config/settings.py

import os
from decouple import config
import dj_database_url # Import the new tool

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- Core Settings ---
SECRET_KEY = config('SECRET_KEY')

# DEBUG is True on your PC, but will be False on Render
DEBUG = 'RENDER' not in os.environ

# --- Deployment Settings ---

# ALLOWED_HOSTS is a security list of who can visit your site.
# We get your new Render URL from an environment variable.
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = config('RENDER_EXTERNAL_HOSTNAME', default=None)
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
else:
    # For local development
    ALLOWED_HOSTS.append('127.0.0.1')


# --- Application definitions ---
INSTALLED_APPS = [
    'main.apps.MainConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Add Whitenoise
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Add Whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'


# --- Database ---
# This is the "smart" logic.
# If it's on Render, it will use the 'DATABASE_URL' environment variable.
# If it's on your PC, it will fall back to your 'db.sqlite3' file.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{os.path.join(BASE_DIR, "db.sqlite3")}'
    )
}

# --- Password validation (no change) ---
AUTH_PASSWORD_VALIDATORS = [ ... ] # (Leave this as it was)

# --- Internationalization (no change) ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# --- Static files (CSS, JavaScript, Images) ---
# This is now configured for Whitenoise
STATIC_URL = 'static/'
STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static') ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Default primary key (no change) ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- POTHIK BONDHU CUSTOM KEYS ---
# We now read this from environment variables
WEATHER_API_KEY = config('WEATHER_API_KEY')