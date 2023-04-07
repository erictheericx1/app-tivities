from django.db import models
from django.contrib.postgres import fields as arrayField
from django.contrib.auth.models import User

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

# --------------------------------------------------------------------------------------------------------------------------------

# CATEGORIES = (
#     ('A', 'Activity category'),
#     ('L', 'Location category'),
# )

# # # compare to toy model 
# class ActivityTag(models.Model):
#     name = models.CharField(max_length=255)
#     color = models.CharField(max_length=20)

# # compare to cat model
# class WishList(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(max_length=255)
#     category = models.CharField(
#         max_length=1,
#         choices=CATEGORIES,
#         default=CATEGORIES[1],
#     )
#     tag = models.ManyToManyField(ActivityTag)

# # compare to feeding model 
# class NewActivity(models.Model):
#     name = models.CharField(max_length=255)
#     location = models.CharField(max_length=255)
#     wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE)
#     complete = models.BooleanField(default=False)






# INTERESTS = (
#     ('Art', 'Art'),
#     ('Music', 'Music'),
#     ('Sports', 'Sports'),
#     ('Games', 'Games'),
#     ('Food', 'Food'),
#     ('Fashion', 'Fashion'),
#     ('Technology', 'Technology'),
#     ('Science', 'Science'),
#     ('Nature', 'Nature'),
#     ('Politics', 'Politics'),
#     ('Religion', 'Religion'),
#     ('History', 'History'),
#     ('Health', 'Health'),
#     ('Fitness', 'Fitness'),
#     ('Space', 'Space'),
# )




# class NewAppUser(models.Model):
#     user = models.ForeignKey(User, related_name="new_app_user", on_delete = models.CASCADE)
#     location = models.CharField(max_length=255)
#     INTEREST_CHOICES = models.CharField(
#         choices=INTERESTS,
#         default=INTERESTS[0],
#     )

# class Location(models.Model):
#     name = models.CharField(max_length=255)
#     state = models.CharField(max_length=255)
#     country = models.CharField(max_length=255)








