from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import User, Activity, UserActivity, AppUser
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# Define the home view
def home(request):
  return render(request, 'welcome.html')

# Define the about view
def about(request):
  return render(request, 'about.html')

# Define the past_activities view
@login_required
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
@login_required
def interests(request, user_id):
  user = User.objects.get(id=user_id)
  appuser = AppUser.objects.get(id=user_id)
  return render(request, 'User/interests.html', {
    'user': user,
    'appuser': appuser,
  })
##not working on new logins? maybe because of the user_id?

class AppUserUpdate(UpdateView):
  model = AppUser
  fields = ['interests']
  success_url = '/user/{user_id}/interests/'

class UserCreate(LoginRequiredMixin, CreateView):
  model = AppUser
  fields = ['interests']
  success_url = '/user/{user.id}/interests/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

# Define the recommend view
@login_required
def recommend(request, user_id):
  user = User.objects.get(id=user_id)
  appuser = AppUser.objects.get(id=user_id)
  recommendation = Activity.objects.filter(interests__overlap=appuser.interests).first()
  return render(request, 'User/recommend.html', {
    'user': user,
    'appuser': appuser,
    'recommendation': recommendation,
  })

# Logging user did activity
# class UserActivityCreate(CreateView):
#   model = UserActivity
#   fields = ['activity']
#   success_url = '/user/<int:user_id>/past_activities/'

#   def form_valid(self, form):
#     form.instance.user = AppUser.objects.get(id=self.request.user.id)
#     return super().form_valid(form)

@login_required
def add_activity(request, user_id, activity_id):
  UserActivity.objects.create(user=AppUser.objects.get(id=user_id), activity=Activity.objects.get(id=activity_id))
  print('activity added')
  return redirect('past_activities', user_id=user_id)


# signup view
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      app_user = AppUser.objects.create(user=user)
      app_user.save()
      login(request, user)
      return redirect('edit_interests', user_id=user.id)
      # return redirect('recommend')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class ActivityCreate(LoginRequiredMixin, CreateView):
  model = Activity
  fields = '__all__'
  success_url = '/activities/'

class ActivityUpdate(LoginRequiredMixin, UpdateView):
  model = Activity
  fields = ['name', 'description', 'interests']

class ActivityDelete(LoginRequiredMixin, DeleteView):
  model = Activity
  success_url = '/activities/'

class ActivityList(LoginRequiredMixin, ListView):
  model = Activity

class ActivityDetail(LoginRequiredMixin, DetailView):
  model = Activity