from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    yahoo_guid = models.CharField(max_length=64)
    yahoo_access_token = models.TextField()

    def __unicode__(self):
        return self.user.first_name

class Review(models.Model):
    user = models.ForeignKey(User)
    restaurant = models.CharField(max_length=254)
    item = models.CharField(max_length=254)
    votes = models.IntegerField()

    def __unicode__(self):
        return self.item
