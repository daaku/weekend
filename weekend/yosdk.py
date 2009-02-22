from weekend.yahoo_oauth import app as yahoo_oauth

import time
import logging
import json


def social_graph(request):
    access_token = request.session['yahoo_access_token']
    params = {
        'q': 'select * from social.profile where guid in (select guid from social.connections where owner_guid=me)',
        'format': 'json',
    }
    response = yahoo_oauth.make_signed_req(YQL_URL, content=params, token=access_token, request=request)
    body = json.loads(unicode(response.read(), 'utf-8'))['query']['results']['profile']
    logging.debug(body[0])
    return body


def updates(request):
    access_token = request.session['yahoo_access_token']
    guid = access_token['xoauth_yahoo_guid']
    descr = "insert description" #FIXME
    title = "insert title" #FIXME
    link = "http://daaku.org" #FIXME
    source = "APP.JUqAuh5g"
    suid = "installed3"
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
