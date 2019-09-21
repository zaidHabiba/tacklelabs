import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'bwl!z5k*xwi=e5p!4ss72$m&4(cvbft+5c(afh+u$g#-*=l*et'

DEBUG = True

ALLOWED_HOSTS = []

from .applications_settings import INSTALLED_APPS
from .middleware_settings import MIDDLEWARE
from .email_settings import EMAIL_BACKEND, EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_PORT, EMAIL_USE_TLS

INSTALLED_APPS = INSTALLED_APPS

MIDDLEWARE = MIDDLEWARE

EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_PORT = EMAIL_PORT
EMAIL_USE_TLS = EMAIL_USE_TLS

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'wsgi.wsgi.application'

from .db_settings import DATABASES

DATABASES = DATABASES

"""
#Azure settings ===[not work]===
AZURE_ACCOUNT_NAME = "csb3c2dc4a76525x42b5xa19"
AZURE_STORAGE_KEY = "S5++mdjWjLcYSLGSEHnPhZXycZYEBYmNFaNdxWtHbzzj+CUIhoRoGd8pBjhmUuqNZI/3ylCarXZUwNXbffxgiQ=="
AZURE_STORAGE_CONTAINER = "media"
AZURE_CONTAINER = "media"

DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

MEDIA_URL = 'http://storage.pepperdeck.com/media/'
"""

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
