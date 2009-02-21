# coding: utf-8
from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from weekend.yahoo_oauth import app as yahoo_oauth
from weekend.fireeagle_oauth import app as fireeagle_oauth

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^oauth/yahoo/', include(yahoo_oauth.urls)),
    (r'^oauth/fireeagle/', include(fireeagle_oauth.urls)),
    (r'', include('weekend.common.urls')),
)
