# coding: utf-8
from django.conf.urls.defaults import patterns
import weekend.common.views as views

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'yql-example/$', views.yql_example),
    (r'restaurants/$', views.restaurants),
    (r'reviews/$', views.reviews),
    (r'review/$', views.add_review),
        
    (r'updates/$', views.updates),
    
    (r'fireeagle-location/$', views.fireeagle_location),
    (r'myspace-oauth/$', views.myspace_opensocial_oauth),
    (r'yelp-reviews/$', views.yelp_data_for_fireeagle_location),

    (r'all-menus/$', views.all_menus_yql),
    (r'dump/$', views.dump),
)
