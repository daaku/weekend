from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response as render
from django.utils.html import escape
from weekend.fireeagle_oauth import app as fireeagle_oauth
from weekend.yahoo_oauth import app as yahoo_oauth
from make_request import make_request
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
    response = yahoo_oauth.make_signed_req(YQL_URL, parameters=params, token=access_token)
    return HttpResponse(unicode(response.read(), 'utf-8'))

def dump(request):
    return HttpResponse('<pre>' + escape(str(request)) + '</pre>')

@fireeagle_oauth.require_access_token
def fireeagle_location(request):
    access_token = request.session['fireeagle_access_token']
    response = fireeagle_oauth.make_signed_req(FIREEAGLE_USER_URL, token=access_token)
    return HttpResponse(unicode(response.read(), 'utf-8'))

@fireeagle_oauth.require_access_token
def yelp_data_for_fireeagle_location(request):
    access_token = request.session['fireeagle_access_token']
    response = fireeagle_oauth.make_signed_req(FIREEAGLE_USER_URL, token=access_token)
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
