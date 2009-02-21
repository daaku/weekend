# coding: utf-8
from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from weekend.yahoo_oauth import app as yahoo_oauth
from weekend.fireeagle_oauth import app as fireeagle_oauth

admin.autodiscover()

import os.path as path
MEDIA_DIR = path.realpath(path.join(path.dirname(__file__), '..', 'media'))

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^oauth/yahoo/', include(yahoo_oauth.urls)),
    (r'^oauth/fireeagle/', include(fireeagle_oauth.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_DIR}),
    (r'', include('weekend.common.urls')),
)
