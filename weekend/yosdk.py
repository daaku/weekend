from weekend.yahoo_oauth import app as yahoo_oauth

import time
import logging
import json
import random
import urllib
YOS_URL='http://social.yahooapis.com/v1'
YQL_URL='http://query.yahooapis.com/v1/yql'

def social_graph(request):
    access_token = request.session['yahoo_access_token']
    params = {
        'q': 'select * from social.profile (0, 9999) where guid in (select guid from social.connections (0, 9999) where owner_guid=me)',
        'format': 'json',
    }
    response = yahoo_oauth.make_signed_req(YQL_URL, content=params, token=access_token, request=request)
    body = json.loads(unicode(response.read(), 'utf-8'))['query']['results']['profile']
    return body

def updates(request, descr, title, link):
    access_token = request.session['yahoo_access_token']
    guid = access_token['xoauth_yahoo_guid']
    source = "APP.JUqAuh5g"
    suid = random.randrange(0, 101)
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
    }''' % (descr, suid, link, source, int(time.time()), title, guid)
    response = yahoo_oauth.make_signed_req("%s/user/%s/updates/%s/%s" % (YOS_URL, guid, source, suid), method='PUT', content=body, token=access_token, request=request)
    return response.status

def geocode(request, location):
    access_token = request.session['yahoo_access_token']
    params = {
        'q': 'select * from geo.places where text="' + location + '"',
        'format': 'json',
    }
    response = yahoo_oauth.make_signed_req(YQL_URL, content=params, token=access_token, request=request)
    body = json.loads(unicode(response.read(), 'utf-8'))['query']['results']['place'][0]['centroid']
    return body
