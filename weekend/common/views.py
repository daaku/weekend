from django.http import HttpResponse
from django.shortcuts import render_to_response as render
from django.utils.html import escape
from weekend.yahoo_oauth import app as yahoo_oauth

YQL_URL='http://query.yahooapis.com/v1/yql'

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
