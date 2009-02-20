from django.conf import settings
from django_oauth_consumer import OAuthConsumerApp

app = OAuthConsumerApp(settings.YAHOO_OAUTH)
