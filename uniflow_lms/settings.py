from pathlib import Path
import os
import dj_database_url # Requirement: dj-database-url
import pymysql
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY SETTINGS ---
# Pulls from Railway Variables; defaults to a dummy key for local dev
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-local-dev-key-123')

# DEBUG should be False in production (Railway Variable DEBUG=False)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS needs to include your Railway domain
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost 127.0.0.1 .up.railway.app').split(' ')

# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Helps WhiteNoise serve static in dev
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    
    # Local apps
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Critical: Must be after SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom Middleware
    'core.middleware.FirstLoginMiddleware',
    'core.middleware.StaffRestrictionMiddleware',
]

ROOT_URLCONF = 'uniflow_lms.urls'

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
                'core.context_processors.notifications_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'uniflow_lms.wsgi.application'

# --- DATABASE CONFIGURATION ---
# Railway provides MYSQL_URL automatically when you add the MySQL service
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('MYSQL_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Fallback to SQLite if no MySQL URL is found (Local Dev)
if not os.environ.get('MYSQL_URL'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

# --- STATIC & MEDIA FILES ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Where files are collected for production
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise storage for compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- AUTHENTICATION & USER ---
AUTH_USER_MODEL = 'core.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- CORS & SECURITY ---
CORS_ALLOW_ALL_ORIGINS = True # Change this to specific domains for better security later

# SSO Secret pulled from Variables
UNIFLOW_SSO_SECRET = os.environ.get('UNIFLOW_SSO_SECRET', 'uNifLow_sSo_2026_shArEd_sEcrEt_kEy')

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# HTTPS Security (Recommended for Railway)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True