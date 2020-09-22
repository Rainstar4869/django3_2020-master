"""
Django settings for exrate2020 project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
import datetime
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

SECRET_KEY = '2us*m@736zhmk@=3!49hm2x#%w4b2v%&n0qktr+r+(esc7hi^%'
# SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = True
# DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

# Application definition
AUTH_USER_MODEL = "authentication.User"

INSTALLED_APPS = [

    'channels',
    "testcelery",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'corsheaders',
    'imagekit',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework',
    'webpack_loader',
    "authentication",
    'django_celery_results',
    'django_celery_beat',
    "expenses",
    "income",
    "userstats",
    "upload",
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',  # This must be first on the list
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',  # This must be last
    'middlewares.setAccessToken.SimpleMiddleware'
]

ROOT_URLCONF = 'exrate2020.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'django_settings_export.settings_export',
            ],
        },
    },
]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
WSGI_APPLICATION = 'exrate2020.wsgi.application'
ASGI_APPLICATION = "exrate2020.routings.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],
        },
    }
}
CACHES = {
    "default": {
        # "BACKEND": "django_redis.cache.RedisCache",
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
        }
    }
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=3),
}
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, './webpack-stats.json'),
        # 'POLL_INTERVAL': 0.1,
        # 'TIMEOUT': None,
        # 'IGNORE': ['.+\.hot-update.js', '.+\.map']
    }
}

BROKER_TRANSPORT_OPTIONS = {
    'visibility_timeout': 3600
}
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_TIMEZONE = 'Asia/Tokyo'
DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'webauth/login/'
LOGOUT_URL = 'webauth/logout/'

SITE_ID = 4

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '991613301101-d7a15n1idf3niaoeef689dil3hiql8gt.apps.googleusercontent.com',
            'secret': 'S9GgCHEmFAYYs7-GT8SjCAYB',
            'key': ''
        }
    }
}

EMAIL_HOST = 'nichiei09.sakura.ne.jp'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'crs@nichiei09.sakura.ne.jp'
EMAIL_HOST_PASSWORD = 'Hisshghu3500'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'crs@nichiei.services'

MESSAGE_TAGS = {
    messages.ERROR: "danger"
}
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# importing logger settings
try:
    from .logger_settings import LOGGING
except Exception as e:
    # in case of any error, pass silently.
    pass

# Nichiei Related
NICHIEI_INFO = {
    "SALES_EMAIL": "crs@nichiei.services",
    "SALES_PHONE": "+81 48 708 6883",
    "SALES_MAN_PHONE": "+81 70-4305-1891",
    "SALES_POSTCODE": "〒336-0031",
    "SALES_ADD": "日本埼玉県さいたま市南区鹿手袋7-19-17"
}


SETTINGS_EXPORT = [
    'NICHIEI_INFO',
]
