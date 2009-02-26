# coding: utf-8
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'daaku.db'))
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
SECRET_KEY = 'm&nDSG45tfdb5yx*=ex=h9byu38p-@lg+lq+*o!#-bqeu30qe!'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
ADMINS = (
    ('Naitik Shah', 'n@daaku.org'),
)
MANAGERS = ADMINS
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = '%s/media' % os.path.dirname(os.path.realpath(__file__))
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/admin/'
APPEND_SLASH = True
AUTHENTICATION_BACKENDS = (
    'weekend.yahoo_oauth.DummyLogin',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.load_template_source',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
ROOT_URLCONF = 'weekend.urls'
INSTALLED_APPS = (
    'weekend.common',

    'django_oauth_consumer',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
)

AUTH_PROFILE_MODULE = 'weekend.models.UserProfile'

from settings_local import *
