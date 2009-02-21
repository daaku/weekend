# coding: utf-8
import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'daaku.db'
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
APPEND_SLASH = False
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
YAHOO_OAUTH = {
    'name': 'yahoo',
    'realm': 'yahooapis.com',
    'request_token_url': 'https://api.login.yahoo.com/oauth/v2/get_request_token',
    'authorization_url': 'https://api.login.yahoo.com/oauth/v2/request_auth',
    'access_token_url': 'https://api.login.yahoo.com/oauth/v2/get_token',
    'consumer_key': 'FIXME',
    'consumer_secret': 'FIXME',
}
FIREEAGLE_OAUTH = {
    'name': 'fireeagle',
    'request_token_url': 'https://fireeagle.yahooapis.com/oauth/request_token',
    'authorization_url': 'https://fireeagle.yahoo.net/oauth/authorize',
    'access_token_url': 'https://fireeagle.yahooapis.com/oauth/access_token',
    'consumer_key': 'FIXME',
    'consumer_secret': 'FIXME',
}
INSTALLED_APPS = (
    'weekend.common',

    'django_oauth_consumer',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
)
