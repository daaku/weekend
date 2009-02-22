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

import weekend.yosdk as yosdk
import collections
import json

YQL_URL='http://query.yahooapis.com/v1/yql'
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
    response = yahoo_oauth.make_signed_req(
        YQL_URL,
        content=params,
        token=access_token,
        request=request,
    )
    return HttpResponse(unicode(response.read(), 'utf-8'))

def dump(request):
    return HttpResponse('<pre>' + escape(str(request)) + '</pre>')

@yahoo_oauth.require_access_token
@fireeagle_oauth.require_access_token
def fireeagle_location(request):
    access_token = request.session['fireeagle_access_token']
    response = fireeagle_oauth.make_signed_req(
        FIREEAGLE_USER_URL,
        token=access_token,
        request=request,
    )
    return HttpResponse(unicode(response.read(), 'utf-8'))

@yahoo_oauth.require_access_token
@fireeagle_oauth.require_access_token
def yelp_data_for_fireeagle_location(request):
    access_token = request.session['fireeagle_access_token']
    response = fireeagle_oauth.make_signed_req(
        FIREEAGLE_USER_URL,
        token=access_token,
        request=request,
    )
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
    response = yahoo_oauth.make_signed_req(
        YQL_URL,
        content=params,
        token=access_token,
        request=request,
    )
    return HttpResponse(unicode(response.read(), 'utf-8'))

@yahoo_oauth.require_access_token
@fireeagle_oauth.require_access_token
def restaurants(request):
    access_token = request.session['fireeagle_access_token']
    response = fireeagle_oauth.make_signed_req(
        FIREEAGLE_USER_URL,
        token=access_token,
        request=request,
    )
    body = unicode(response.read(), 'utf-8')
    cordinates = json.loads(body)['user']['location_hierarchy'][0]['geometry']['coordinates']

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

    response = yahoo_oauth.make_signed_req(
        YQL_URL,
        content=params,
        token=access_token,
        request=request,
    )
    body = unicode(response.read(), 'utf-8')
    restaurants = json.loads(body)['query']['results']['Result']
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


@fireeagle_oauth.require_access_token
def places(request):
    # [[tl_long, tl_lat], [br_long, br_lat]] = json.loads(loc)['user']['location_hierarchy'][1]['geometry']['bbox']
    access_token = request.session['fireeagle_access_token']
    response = fireeagle_oauth.make_signed_req(
        FIREEAGLE_USER_URL,
        token=access_token,
        request=request,
    )
    body = unicode(response.read(), 'utf-8')
    cordinates = json.loads(body)['user']['location_hierarchy'][0]['geometry']['coordinates']
    if(cordinates):
      [ lon, lat ] = cordinates
    else:
      [ lon, lat ] = cordinates[0]

    # places = get_places(br_lat, br_long, tl_lat, tl_long)
    places = [
        {'name':'restaurant A','addr':'1 this ave, sunnyvale, ca 94098','id':'restauranta'},
        {'name':'cafe B','addr':'239840 that st., mountain view, ca 98231','id':'cafeb'},
        {'name':'dive C','addr':'3 nonce rd., san jose, ca 90801','id':'divec'}
    ]
    return render('common/places.html', {'places':places});

# @yahoo_oauth.require_access_token
def menu(request):
    pid = request.GET['pid']
    # get_menu(pid)
    # reviews = get_reviews(pid)
    menu = [
        {
            'iid':pid+'itema',
            'name':'item a',
            'price':1.00,
            'reviews':{
                'total':{'up':2,'dn':1},
                'by_name': [
                    {'uid':'guid1', 'name':'friend 1', 'img':'http://...sjdlfj.jpg', 'vote':1},
                    {'uid':'guid2', 'name':'friend 2', 'img':'http://...friend2.jpg', 'vote':1},
                    {'uid':'guid3', 'name':'friend 3', 'img':'http://...friend3.jpg', 'vote':0}
                ]
            }
        },
        {
            'iid':pid+'itemb',
            'name':'item b',
            'price':2.50,
            'reviews':{
                'total': {'up':1,'dn':2},
                'by_name': [
                    {'uid':'guid4', 'name':'friend 4', 'img':'http://...friend4.jpg', 'vote':0},
                    {'uid':'guid2', 'name':'friend 2', 'img':'http://...friend2.jpg', 'vote':0},
                    {'uid':'guid6', 'name':'friend 6', 'img':'http://...friend6.jpg', 'vote':1}
                ]
            }
        },
        {
            'iid':pid+'pepsi',
            'name':'pepsi',
            'price':4.00,
            'reviews':{
                'total': {'up':2,'dn':0},
                'yours':1,
                'by_name': [
                    {'uid':'guid3', 'name':'friend 3', 'img':'http://...friend3.jpg', 'vote':1},
                    {'uid':'guid6', 'name':'friend 6', 'img':'http://...friend6.jpg', 'vote':1}
                ]
            }
        }
    ]

    return render('common/menu.html', {'menu':menu});

def vote(request):
    return HttpResponse(unicode('voted!', 'utf-8'))
