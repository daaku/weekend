from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django_oauth_consumer import OAuthConsumerApp
from functools import wraps
from weekend.common.models import UserProfile
import json
import logging


class DBOAuthConsumerApp(OAuthConsumerApp):
    def require_access_token(self, view):
        access_token_key = self.name + '_access_token'
        next_url_key = self.name + '_next_url'
        needs_auth_view = self.name + '_needs_auth'

        @wraps(view)
        def _do(request, *args, **kwargs):
            if access_token_key in request.session:
                return view(request, *args, **kwargs)

            if request.user and request.user.is_authenticated():
                try:
                    profile = request.user.get_profile()
                    if profile.yahoo_access_token:
                        request.session[access_token_key] = json.loads(profile.yahoo_access_token)
                        return view(request, *args, **kwargs)
                except:
                    pass

            request.session[next_url_key] = request.get_full_path()
            return HttpResponseRedirect(reverse(needs_auth_view))

        return _do

    def create_or_update_yahoo_user(self, access_token, request, **kwargs):
        guid = access_token['xoauth_yahoo_guid']
        json_access_token = json.dumps(access_token)
        if request.user and request.user.is_anonymous():
            user, created = User.objects.get_or_create(username=guid)
            request.user = user
            profile, created = UserProfile.objects.get_or_create(yahoo_guid=guid, user=user)
            profile.yahoo_access_token = json_access_token
            profile.save()

app = DBOAuthConsumerApp(settings.YAHOO_OAUTH)
app.got_access_token.connect(app.create_or_update_yahoo_user)
