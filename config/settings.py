from datetime import timedelta
import os
from pathlib import Path
from dotenv import load_dotenv
from str2bool import str2bool
import dj_database_url

load_dotenv()  # take environment variables from .env.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

### Security Settings ###

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'Super_Secr3t_9999')

# Enable/Disable DEBUG Mode
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')
CSRF_TRUSTED_ORIGINS = os.getenv(
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost:8000,http://127.0.0.1:8000'
).split(',')

### Installed Apps ###

INSTALLED_APPS = [

    # Volt Admin Theme
    'admin_volt.apps.AdminVoltConfig',

    # Tables
    'django_tables2',
    
    # Security & Access Control
    # 'axes',
    
    # API Documentation
    'drf_spectacular',

    # Django Core
    "django.contrib.humanize",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    
    # Developer Tools
    'django_extensions',
    'django_filters',
    
    # Admin / Theme
    'jazzmin',

    # Database Enhancements
    'django.contrib.postgres',
    'psqlextra',

    # API & Auth
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    
    # Project Apps
    'apps.core',
    'apps.dashboard',
    'apps.location',
    'apps.attendance',
    'apps.appversion',
    'apps.users',
    'apps.overtime',

    # UI & Forms Styling
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
]

### Middleware ###

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'axes.middleware.AxesMiddleware',
]

AUTHENTICATION_BACKENDS = [
    # 'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = "config.urls"

### Templates Configuration ###

HOME_TEMPLATES = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [HOME_TEMPLATES],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = ["bootstrap5"]
CRISPY_TEMPLATE_PACK = "bootstrap5"

### Database ###

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    db_config = dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
    )
    db_config['ENGINE'] = 'psqlextra.backend'
    DATABASES = {
        'default': db_config,
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'psqlextra.backend',
            'NAME': os.getenv('DB_NAME', 'postgres'),
            'USER': os.getenv('DB_USERNAME', 'admin'),
            'PASSWORD': os.getenv('DB_PASS', 'password'),
            'HOST': os.getenv('DB_HOST', 'orbit-db'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }

### Caches (Redis) ###

REDIS_URL = os.getenv('REDIS_URL', 'redis://orbit-redis:6379/1')
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

### Password validation ###

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# WHITE NOISE
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
WHITENOISE_KEEP_ONLY_HASHED_FILES = True

### Internationalization ###

LANGUAGE_CODE = "en-us"
LANGUAGES = [
    ('en', 'English'),
    ('ar', 'Arabic'),
]
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]
TIME_ZONE = "Asia/Damascus"
USE_I18N = True
USE_TZ = True

### Static files (CSS, JavaScript, Images) ###

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


### Login & Email Settings ###

LOGIN_URL = '/users/accounts/login/'
LOGIN_REDIRECT_URL = '/'

### REST Framework & JWT Configuration ###

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '60/minute',
        'anon': '10/minute'
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

AUTH_USER_MODEL = 'users.User'


### Security & Cookies ###

if not DEBUG:
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True

#Enable Secure Flag For All Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

#Enable Http Only For All Cookies
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

#Enable SameSite To Prevent CSRF Attacks
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# Set security headers to prevent caching
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

### Django Axes Configuration ###

#Axes Setting For Block User After 5 Failure Tries
# AXES_FAILURE_LIMIT = 5
# AXES_COOLOFF_TIME = timedelta(minutes=10)
# AXES_LOCK_OUT_AT_FAILURE = True
# AXES_VERBOSE = False
# AXES_LOCKOUT_CALLABLE = 'apps.core.views.custom_lockout_view'

### Default primary key field type ###

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

### Partitioning ###

PSQLEXTRA_PARTITIONING_MANAGER = "partitioning.manager.manager"

### DYNAMIC_DATATB Settings ###

DYNAMIC_DATATB = {
    # SLUG -> Import_PATH 
    # 'Countries': 'apps.configuration.models.Country',
    # 'Cities': 'apps.configuration.models.City',
    # 'Payment Methods': 'apps.configuration.models.PaymentMethod',
    # 'Users': 'apps.core.models.User',
    # 'Profiles': 'apps.profiles.models.Profile',
    # 'Orders': 'apps.order.models.Order',
    # 'Workers': 'apps.worker.models.Worker',
    # 'Notification': 'apps.notification.models.Notification',
    # 'Service': 'apps.services.models.Service',
    # 'Home Service Image': 'apps.services.models.HomeServiceImage',
    
}

#SMS API Configuration
SMS_API_URL = os.getenv('SMS_API_URL')
SMS_API_USERNAME = os.getenv('SMS_API_USERNAME')
SMS_API_PASSWORD = os.getenv('SMS_API_PASSWORD')

#Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'host44.registrar-servers.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# OTP Management Settings
MAX_ATTEMPTS = int(os.getenv('MAX_ATTEMPTS', 5))
BLOCK_DURATION = int(os.getenv('BLOCK_DURATION', 30))
RETRY_DURATION = int(os.getenv('RETRY_DURATION', 20))
OTP_EXPIRATION = int(os.getenv('OTP_EXPIRATION', 20))

# Attendance App Settings
COMPANY_LATITUDE = 33.513807
COMPANY_LONGITUDE = 36.276527
COMPANY_RADIUS_METERS = 150
WEEKEND_DAYS = [0]  # Friday=4, Saturday=5 (Django: Monday=0)