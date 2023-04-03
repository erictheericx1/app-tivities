from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import User, Activity, UserActivity

# Create your views here.

# Define the home view
def home(request):
  return render(request, 'welcome.html')

# Define the about view
def about(request):
  return render(request, 'about.html')

# Define the past_activities view
def past_activities(request, user_id):
  user = User.objects.get(id=user_id)
  past_activities = UserActivity.objects.filter(user=user)
  return render(request, 'past_activities.html', {
    'user': user,
    'past_activities': past_activities
  })

# Define the interests view
def interests(request, user_id):
  user = User.objects.get(id=user_id)
  interests = User.objects.get(id=user_id).interests
  return render(request, 'interests.html', {
    'user': user,
    'interests': interests
  })

class UserUpdate(UpdateView):
  model = User
  fields = ['interests']
  success_url = '/user/<int:user_id>/interests/'

# Define the recommend view
def recommend(request, user_id):
  user = User.objects.get(id=user_id)
  return render(request, 'recommend.html', {
    'user': user
  })