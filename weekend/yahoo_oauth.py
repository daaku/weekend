from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django_oauth_consumer import OAuthConsumerApp, NoAccessToken
from functools import wraps
from weekend.common.models import UserProfile
import json
import logging


class DummyLogin(ModelBackend):
    def authenticate(self, **kwargs):
        if 'guid' in kwargs:
            user, created = User.objects.get_or_create(username=guid, password=guid)
            return user
        else:
            return super(DummyLogin, self).authenticate(**kwargs)

class DBOAuthConsumerApp(OAuthConsumerApp):
    def store_access_token(self, request, token):
        guid = token['xoauth_yahoo_guid']
        user = authenticate(guid=guid)
        login(request, user)
        json_token = json.dumps(token)
        profile, created = UserProfile.objects.get_or_create(
            yahoo_guid=guid,
            user=user,
            defaults={'yahoo_access_token': json_token})

    def get_access_token(self, request):
        if request.user and request.user.is_authenticated():
            profile = UserProfile.objects.get(user=request.user)
            return json.loads(profile.yahoo_access_token)
        raise NoAccessToken()

app = DBOAuthConsumerApp(settings.YAHOO_OAUTH)
