from django.db import models
from django.contrib.postgres import fields as arrayField

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    interests = arrayField.ArrayField(models.CharField(max_length=255), blank=True, null=True)

class Activity(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    interests = arrayField.ArrayField(models.CharField(max_length=255), blank=True, null=True)

class UserActivity(models.Model):
    user = models.ForeignKey(User, related_name="activity_user", on_delete = models.CASCADE)
    activity = models.ForeignKey(Activity, related_name="user_activity", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# to find all activities that match the user's interests, use the following query:
# Activity.objects.filter(interests__overlap=user.interests)