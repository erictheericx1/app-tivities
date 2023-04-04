from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import User, Activity, UserActivity, AppUser

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
  past_activities = UserActivity.objects.filter(user_id=user_id)
  arr = []
  for activity in past_activities:
    arr.append(Activity.objects.get(id=activity.activity_id))
  return render(request, 'User/past_activities.html', {
    'user': user,
    'acts': arr,
  })

# Define the interests view
def interests(request, user_id):
  user = User.objects.get(id=user_id)
  appuser = AppUser.objects.get(id=user_id)
  return render(request, 'User/interests.html', {
    'user': user,
    'appuser': appuser,
  })

class UserUpdate(UpdateView):
  model = AppUser
  fields = ['interests']
  success_url = '/user/<int:user_id>/interests/'

class UserCreate(CreateView):
  model = AppUser
  fields = ['interests']
  success_url = '/user/<int:user_id>/interests/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

# Define the recommend view
def recommend(request, user_id):
  user = User.objects.get(id=user_id)
  appuser = AppUser.objects.get(id=user_id)
  recommendation = Activity.objects.filter(interests__overlap=appuser.interests).first()
  return render(request, 'User/recommend.html', {
    'user': user,
    'appuser': appuser,
    'recommendation': recommendation,
  })

class UserActivityCreate(CreateView):
  model = UserActivity
  fields = ['activity']
  success_url = '/user/<int:user_id>/past_activities/'

  def form_valid(self, form):
    form.instance.user = AppUser.objects.get(id=self.request.user.id)
    return super().form_valid(form)