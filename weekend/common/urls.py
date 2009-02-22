# coding: utf-8
from django.conf.urls.defaults import patterns
import weekend.common.views as views

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'yql-example/$', views.yql_example),
 
    (r'places/$', views.places),
    (r'menu/$', views.menu),
    (r'vote/$', views.vote),

    (r'reviews/$', views.reviews),
    (r'review/$', views.add_review),
    (r'fireeagle-location/$', views.fireeagle_location),
    (r'yelp-reviews/$', views.yelp_data_for_fireeagle_location),
    (r'all-menus/$', views.all_menus_yql),
    (r'dump/$', views.dump),

)
