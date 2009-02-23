from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
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
from urlencoding import parse_qs, compose_qs
from urllib import quote

import weekend.yosdk as yosdk
import collections
import json
import logging

YQL_URL='http://query.yahooapis.com/v1/yql'
YQL_PUBLIC_URL='http://query.yahooapis.com/v1/public/yql'
FIREEAGLE_USER_URL='https://fireeagle.yahooapis.com/api/0.1/user.json'
YELP_REVIEW_URL='http://api.yelp.com/business_review_search'

def index(request):
    return render('common/index.html')

@yahoo_oauth.require_access_token
def location(request):
    location = yosdk.geocode(request, request.GET['address'])
    lat = location['latitude']
    lon = location['longitude']

    return HttpResponseRedirect("/places/?lat=%s&lon=%s" % (lat, lon))

@fireeagle_oauth.require_access_token
def fireeagle_location(request):
    access_token = request.session['fireeagle_access_token']
    response = fireeagle_oauth.make_signed_req(
        FIREEAGLE_USER_URL,
        token=access_token,
        request=request,
    )
    body = unicode(response.read(), 'utf-8')
    cordinates = json.loads(body)['user']['location_hierarchy'][0]['geometry']['coordinates']
    if isinstance(cordinates[0], list) and isinstance(cordinates[0][0], list):
        (lon, lat) = cordinates[0][0]
    elif isinstance(cordinates[0], list):
        (lon, lat) = cordinates[0]
    else:
        (lon, lat) = cordinates
    return HttpResponseRedirect("/places/?lat=%s&lon=%s" % (lat, lon))

def items_in_graph(request, restaurant):
    profiles = {}
    for p in yosdk.social_graph(request):
        profiles[p['guid']] = p
    profiles['BJTDY5GOXXOBRASYLIGD4WUDM4'] = {
        'guid': 'BJTDY5GOXXOBRASYLIGD4WUDM4',
        'nickname': 'Chirag',
        'image': {
            'imageUrl': 'http://F3.yahoofs.com/coreid/4917386ai946zul7sp1/HG3DMu86cLXmekhOh1KGhF8-/3/t192.png?ciAQpxKB_xQNbneN'
        }
    }
    friends = User.objects.filter(username__in=profiles.keys())
    reviews = Review.objects.filter(user__in=friends)
    logging.error(reviews)
    to_return = []
    for review in reviews:
        profile = profiles[review.user.username]
        logging.debug(restaurant)
        logging.debug(review.restaurant)
        if restaurant == review.restaurant:
            to_return.append({
                'guid': profile['guid'],
                'nickname': profile['nickname'],
                'pic': profile['image']['imageUrl'],
                'item': review.item,
                'restaurant': review.restaurant,
                'votes': review.votes,
            })
    return to_return

def places(request):
    if 'lat' in request.GET and 'lon' in request.GET:
        lat = request.GET['lat']     # 37.4248085022
        lon = request.GET['lon']     # -122.074012756
  
        params = {
            'q': "select * from xml where url='http://api.boorah.com/restaurants/WebServices/RestaurantSearch?radius=15&sort=distance&start=0&lat=%s&long=%s&auth=%s' and itemPath = 'Response.ResultSet.Result'" % (lat, lon, settings.BOORAH_API_KEY),
            'format': 'json',
        }

        response = json.loads(unicode(yahoo_oauth.make_signed_req(YQL_PUBLIC_URL, content=params).read(), 'utf-8'))

        if 'query' in response:
            restaurants = response['query']['results']['Result']
        else:
            restaurants = []
        
        return HttpResponse(render('common/places.html', { 'places': restaurants }))

    else:
        return HttpResponseRedirect('/')

@yahoo_oauth.require_access_token
def menu(request):

    if 'lat' in request.GET and 'lon' in request.GET and 'restaurant' in request.GET:

        lat = request.GET['lat']                   # 37.4248085022
        lon = request.GET['lon']                   # -122.074012756
        restaurant = request.GET['restaurant']     # Country Deli
        restaurantName= request.GET['restaurant']     # Country Deli

        friends = items_in_graph(request, restaurant)
  
        params = {
            'q': "select * from xml where url='http://api.boorah.com/restaurants/WebServices/RestaurantSearch?radius=15&sort=distance&start=0&lat=%s&long=%s&name=%s&auth=%s' and itemPath = 'Response.ResultSet.Result'" % (lat, lon, quote(restaurant), settings.BOORAH_API_KEY),
            'format': 'json',
        }
        response = json.loads(unicode(yahoo_oauth.make_signed_req(YQL_PUBLIC_URL, content=params).read(), 'utf-8'))
        
        menu = []
        try:

            # get restaurant json - then fetch menu url - then fetch yql menu

            # allmenus_yql = select * from html where url='http://www.allmenus.com/ca/mountain-view/123349-quiznos-sub/menu/' and xpath='//div[@class="menu_item"]'
            # menupages_yql = select * from html where url='http://www.menupages.com/Partnermenu.asp?partner=7&restaurantId=10522&t=1235342717&auth=4b479e7b075fef07b533cd1acee30369' and xpath='//div[@id="restaurant-menu"]/table/tbody/tr/th'

	    restaurant = response['query']['results']['Result'][0]
            link = restaurant['LinkSet']['Link']
                
            if link['type'] == 'menu':
                params = {
                    'q': "select * from html where url='%s' and xpath = '//iframe'" % (link['url']),
                    'format': 'json',
                }
                menu = json.loads(unicode(yahoo_oauth.make_signed_req(YQL_PUBLIC_URL, content=params).read(), 'utf-8'))['query']['results']['iframe']['src']

                if 'allmenus' in menu:

                    response = yahoo_oauth.make_signed_req(menu)
                    response = yahoo_oauth.make_signed_req('http://allmenus.com' + response.getheader('location'))
                
                    params = {
                        'q': "select * from html where url='%s' and xpath='//div[@class=\"menu_item\"]'" % ('http://allmenus.com' + response.getheader('location')),
                        'format': 'json',
                    }

                    data = json.loads(unicode(yahoo_oauth.make_signed_req(YQL_PUBLIC_URL, content=params).read(), 'utf-8'))
                    menu = data['query']['results']['div']

                
        except:

            pass

        return HttpResponse(render('common/menu.html', { 'menu': menu, 'friends': friends, 'restaurant': restaurantName  }))

    else:
      
        return HttpResponseRedirect('/')


    return HttpResponse()


@yahoo_oauth.require_access_token
def add_review(request):
    if request.method == 'POST':
        base_review = Review(user=request.user)
        form = ReviewForm(request.POST, instance=base_review)
        if form.is_valid():
            review = form.save()
            yosdk.updates(
                request,
                " add the item " + review.item + " for the restaurant " + review.restaurant,
                "", #FIXME
                "http://weekend.daaku.org/"
             )
            return HttpResponseRedirect('/reviews/')
    else:
        form = ReviewForm()
    return HttpResponse(render('common/review.html', {'form': form}))


@yahoo_oauth.require_access_token
def reviews(request):
    return HttpResponse()


def vote(request):
    return HttpResponse(unicode('voted!', 'utf-8'))
