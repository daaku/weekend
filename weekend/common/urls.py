# coding: utf-8
from django.conf.urls.defaults import patterns
import weekend.common.views as views

urlpatterns = patterns('',
    (r'^$', views.index),

    (r'places/$', views.places),
    (r'menu/$', views.menu),
    (r'vote/$', views.vote),

    (r'items/$', views.items_in_graph),
    (r'reviews/$', views.reviews),
    (r'review/$', views.add_review),
    (r'fireeagle-location/$', views.fireeagle_location),

    (r'location/$', views.location),
)
