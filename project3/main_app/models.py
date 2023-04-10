from django.db import models
from django.contrib.postgres import fields as arrayField
from django.contrib.auth.models import User

# default_interests = ('Art', 'Music', 'Sightseeing', 'Shopping', 'Restaurants', 'Bars', 'Events', 'Outdoor Recreation', 'History', 'Nature', 'Education', 'Fitness', 'Travel', 'Books', 'Photography', 'Theater', 'Architecture', 'Cuisine', 'Local Culture', 'Street Markets', 'Museums', 'Urban Exploration', 'City Parks', 'Public Transportation')

default_interests = ('Art', 'Music', 'Sports', 'Games', 'Food', 'Travel', 'Fashion', 'Technology', 'Science', 'Nature', 'Politics', 'Religion', 'History', 'Education', 'Health', 'Fitness', 'Space', 'Cars', 'Bars', 'Photography', 'Painting', 'Writing', 'Reading')

# Create your models here.
class AppUser(models.Model):
    user = models.ForeignKey(User, related_name="app_user", on_delete = models.CASCADE)
    interests = arrayField.ArrayField(models.CharField(max_length=255), blank=True, null=True, default = [])
    all_interests = arrayField.ArrayField(models.CharField(max_length=255), blank=True, null=True, default=default_interests)

class Activity(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    interests = arrayField.ArrayField(models.CharField(max_length=255), blank=True, null=True)

class Wish(models.Model):
    user = models.ForeignKey(AppUser, related_name="wish_user", on_delete = models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    interests = arrayField.ArrayField(models.CharField(max_length=255), blank=True, null=True)

class UserActivity(models.Model):
    user = models.ForeignKey(AppUser, related_name="activity_user", on_delete = models.CASCADE)
    activity = models.ForeignKey(Wish, related_name="user_activity", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)





