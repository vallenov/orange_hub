import os
import sys

try:
    import local_settings
except ImportError:
    local_settings = None

DEBUG = getattr(local_settings, 'LOCAL_DEBUG', True)

ALLOWED_HOSTS = ['*']

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(PROJECT_PATH, 'apps'))

ROOT_URLCONF = 'urls'

SECRET_KEY = getattr(local_settings, 'LOCAL_SECRET_KEY', '')

ESP_HUB_HOST = getattr(local_settings, 'ESP_HUB_HOST', 'http://0.0.0.0')

STATIC_URL = '/static/'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [
            'polls/templates'
        ]
    },
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    #'admin',
    'web_auth',
    'light',
    'hub_screen',
]

MIDDLEWARE = [
    'utils.log.middleware.LogRequestMiddleware',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_filter': {
            '()': 'utils.log.filters.RequestFilter',
        },
    },
    'formatters': {
        'request_formatter': {
            'format': '{asctime:s} '
                      '[{process:d}]: '
                      '[{levelname:s}] '
                      '{name:s} '
                      '"{message:s}"',
            'style': '{'
        },
    },
    'handlers': {
        'null': {
            'level': 'INFO',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            # 'filters': ['request_filter'],
            'formatter': 'request_formatter',
            # 'stream': 'ext://sys.stdout'
        },
        'file_log': {
            'class': 'logging.handlers.RotatingFileHandler',
            # 'filters': ['request_filter'],
            'formatter': 'request_formatter',
            'filename': 'run.log',
            'mode': 'a',
            'maxBytes': 10485760,
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file_log'],
            'level': 'INFO',
            'propagate': True
        },
        'django.request': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# AUTH_USER_MODEL = 'auth.Users'

