from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response as render
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import escape
from django.contrib.auth.models import User
from make_request import make_request
from weekend.common.models import UserProfile
from weekend.common.models import Review
from weekend.common.forms import ReviewForm
from weekend.fireeagle_oauth import app as fireeagle_oauth
from weekend.yahoo_oauth import app as yahoo_oauth

import collections
import time
import json

YQL_URL='http://query.yahooapis.com/v1/yql'
YOS_URL='http://social.yahooapis.com/v1'
FIREEAGLE_USER_URL='https://fireeagle.yahooapis.com/api/0.1/user.json'
YELP_REVIEW_URL='http://api.yelp.com/business_review_search'

def index(request):
    return render('common/index.html')

@yahoo_oauth.require_access_token
def yql_example(request):
    access_token = request.session['yahoo_access_token']
    params = {
        'q': 'select * from social.profile where guid in (select guid from social.connections where owner_guid=me)',
        'format': 'json',
    }
    response = yahoo_oauth.make_signed_req(YQL_URL, parameters=params, token=access_token, request=request)
    return HttpResponse(unicode(response.read(), 'utf-8'))

def dump(request):
    return HttpResponse('<pre>' + escape(str(request)) + '</pre>')

@yahoo_oauth.require_access_token
@fireeagle_oauth.require_access_token
def fireeagle_location(request):
    access_token = request.session['fireeagle_access_token']
    response = fireeagle_oauth.make_signed_req(FIREEAGLE_USER_URL, token=access_token, request=request)
    return HttpResponse(unicode(response.read(), 'utf-8'))

@yahoo_oauth.require_access_token
@fireeagle_oauth.require_access_token
def yelp_data_for_fireeagle_location(request):
    access_token = request.session['fireeagle_access_token']
    response = fireeagle_oauth.make_signed_req(FIREEAGLE_USER_URL, token=access_token, request=request)
    body = unicode(response.read(), 'utf-8')
    user = json.loads(body)
    [[tl_long, tl_lat], [br_long, br_lat]] = json.loads(body)['user']['location_hierarchy'][0]['geometry']['bbox']
    response = make_request(YELP_REVIEW_URL, content={
        'term': 'pizza',
        'br_lat': br_lat,
        'br_long': br_long,
        'tl_lat': tl_lat,
        'tl_long': tl_long,
        'radius': 5,
        'ywsid': settings.YELP_KEY,
    })
    return HttpResponse(unicode(response.read(), 'utf-8'))

@yahoo_oauth.require_access_token
def all_menus_yql(request):
    yql = """
    select * from html where url="http://www.allmenus.com/ca/palo-alto/46901-osteria/menu/" and xpath='//div[@class="menu_item"]/span'
    """
    access_token = request.session['yahoo_access_token']
    params = {
        'q': yql,
        'format': 'json',
    }
    response = yahoo_oauth.make_signed_req(YQL_URL, parameters=params, token=access_token, request=request)
    return HttpResponse(unicode(response.read(), 'utf-8'))

@yahoo_oauth.require_access_token
@fireeagle_oauth.require_access_token
def restaurants(request):
  
    access_token = request.session['fireeagle_access_token']
    cordinates = json.loads(unicode(fireeagle_oauth.make_signed_req(FIREEAGLE_USER_URL, token=access_token, request=request).read(), 'utf-8'))['user']['location_hierarchy'][0]['geometry']['coordinates']
    
    if(cordinates):
      [ lon, lat ] = cordinates
    else:
      [ lon, lat ] = cordinates[0]

    yql = "select * from xml where url='http://api.boorah.com/restaurants/WebServices/RestaurantSearch?radius=5&sort=distance&start=0&lat=%s&long=%s&auth=%s' and itemPath = 'Response.ResultSet.Result'" % (lat, lon, settings.BOORAH_API_KEY)

    access_token = request.session['yahoo_access_token']
    params = {
        'q': yql,
        'format': 'json',
    }

    restaurants = json.loads(unicode(yahoo_oauth.make_signed_req(YQL_URL, parameters=params, token=access_token, request=request).read(), 'utf-8'))['query']['results']['Result']
    params = {
        'q': "select * from html where url='http://www.boorah.com/restaurants/mpMenu.jsp?rid=4756&restid=10522' and xpath='//iframe'",
        'format': 'json',
    }

    return HttpResponse(render('common/restaurants.html', { 'restaurants': restaurants }))

@yahoo_oauth.require_access_token
@fireeagle_oauth.require_access_token
def reviews(request):

    return HttpResponse()


@yahoo_oauth.require_access_token    
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)        
        if form.is_valid():
            # review = Review.objects.get(pk=1)
            # form = ReviewForm(instance=review)
            form.save()
            return HttpResponseRedirect('/reviews/')
    else:
        form = ReviewForm()
    return HttpResponse(render('common/review.html', {'form': form}))


def get_or_create_profile(user):
  try:
      profile = user.get_profile()
  except ObjectDoesNotExist:
      profile = UserProfile(guid='12345667890', user=user)
      profile.save()
  return profile

@yahoo_oauth.require_access_token
def updates(request):
    access_token = request.session['yahoo_access_token']
    guid = access_token['xoauth_yahoo_guid']
    descr = "insert description" #FIXME
    title = "insert title" #FIXME
    link = "http://daaku.org" #FIXME
    source = "APP.JUqAuh5g"
    suid = "installed"
    body = '''
{ "updates": 
  [
    {
      "class": "app",
      "collectionType": "guid",
      "description": "%s",
      "suid": "%s",
      "link": "%s",
      "source": "%s",
      "pubDate": "%s",
      "title": "%s",
      "type": "appActivity",
      "collectionID": "%s"  
    }
  ]
}''' % (descr, suid, link, source, time.time(), title, guid)
    response = yahoo_oauth.make_signed_req_raw("%s/user/%s/updates/%s/%s" % (YOS_URL, guid, source, suid), method='PUT', body=body, token=access_token)
    return HttpResponse(unicode(response.read(), 'utf-8'))
