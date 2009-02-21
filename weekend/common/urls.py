# coding: utf-8
from django.conf.urls.defaults import patterns
import weekend.common.views as views

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'yql-example/$', views.yql_example),
    (r'fireeagle-location/$', views.fireeagle_location),
    (r'dump/$', views.dump),
)
