from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    guid = models.CharField(max_length=64)
    access_token = models.CharField(max_length=128)
    
class Review(models.Model):
    user = models.ForeignKey(User)
    restaurant = models.CharField(max_length=254)
    stars = models.IntegerField()
    content = models.CharField(max_length=1000)
