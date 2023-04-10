from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import openai
import os

from .models import User, Activity, UserActivity, AppUser, Wish 

openai.api_key = os.getenv("OPENAI_API_KEY")

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
    arr.append(Wish.objects.get(id=activity.activity_id))
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

# Define the interests_edit view
@login_required
def interests_edit(request, user_id):
  user = User.objects.get(id=user_id)
  appuser = AppUser.objects.get(id=user_id)
  return render(request, 'User/interests_edit.html', {
    'user': user,
    'appuser': appuser,
  })

# Define the interests_add view
@login_required
def interests_add(request, user_id, interest):
  user = User.objects.get(id=user_id)
  appuser = AppUser.objects.get(id=user_id)
  appuser.interests.append(interest)
  appuser.save()
  return redirect('edit_interest', user_id=user_id)

# Define the interests_remove view
@login_required
def interests_remove(request, user_id, interest):
  user = User.objects.get(id=user_id)
  appuser = AppUser.objects.get(id=user_id)
  appuser.interests.remove(interest)
  appuser.save()
  return redirect('edit_interest', user_id=user_id)


class UserCreate(LoginRequiredMixin, CreateView):
  model = AppUser
  fields = ['interests']
  success_url = '/user/{user.id}/interests/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

# Define the recommend view (non-ai, no longer in use due to reaching stretch goal)
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

# ------------------------- #
# Activity CRUD 
# ------------------------- #


@login_required
def add_activity(request, user_id, activity_id):
  UserActivity.objects.create(user=AppUser.objects.get(id=user_id), activity=Wish.objects.get(id=activity_id))
  print('activity added')
  return redirect('past_activities', user_id=user_id)

class ActivityCreate(LoginRequiredMixin, CreateView):
  model = Activity
  fields = '__all__'
  success_url = '/activity/'

class ActivityUpdate(LoginRequiredMixin, UpdateView):
  model = Activity
  fields = ['name', 'description', 'interests']
  success_url = '/activity/'

class ActivityDelete(LoginRequiredMixin, DeleteView):
  model = Activity
  success_url = '/activity/'

class ActivityList(ListView):
  model = Activity

def activity_deets(request, wish_str):
  a = Activity.objects.get(name=wish_str)
  return redirect('activity_detail', pk=a.id)

class ActivityDetail(LoginRequiredMixin, DetailView):
  model = Activity

# ------------------------- #
# login  
# ------------------------- #

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      app_user = AppUser.objects.create(user=user)
      app_user.save()
      login(request, user)
      return redirect('recommend', user_id=user.id)
      # return redirect('recommend')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)



# ------------------------- #
# ai stuff  
# ------------------------- #

def ai_rec(request, user_id):
    if request.method == 'POST':
        location = request.POST.get('location')
        interests = AppUser.objects.get(id=user_id).interests
        print(f"User interests: {interests}")
        prompt = f""" 
        Your job is to return fun activites for a user to do based on their location and interests, focusing more on the location over the interests. list the activity as new lines
        eg. \n Walk to the beach \n Go to the park
        location: {location}
        interests: {interests}
        activities: """
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=["<DONE>"]
        )
        activities = response.choices[0].text
        activity_list = activities.split('\n')
        activity_list = [activity.strip() for activity in activity_list if activity != '']
        print(f"AI Activity List: {activity_list}")

        appuser = AppUser.objects.get(id=user_id)
        return render(request, 'User/recommend.html', {
          'recommendation': activity_list,
          'appuser': appuser,
          }) 
    else:
        return HttpResponse('Cant generate activity ideas. 404 page coming soon....')


def add_wishlist(request, user_id, activity_str):
  if request.method == 'POST':
    prompt = f""" 
      Your job is to return a description of this activity in 2 sentences.
      activity: {activity_str}
      description: """

    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      temperature=0.9,
      max_tokens=100,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0.6,
      stop=["<DONE>"]
    )
    description = response.choices[0].text
    print(description)
    w = Wish.objects.create(user=AppUser.objects.get(id=user_id), name=activity_str, description=description, interests=[])
    w.save()
    a = Activity.objects.create(name=activity_str, description=description, interests=[])
    a.save()

    return redirect('user_wishlist', user_id=user_id)
  else:
    return HttpResponse('Cant add to wishlist. 404 coming soon......')
  
# ------------------------- #
# wishlist   
# ------------------------- #

def user_wishlist(request, user_id):
  appuser = AppUser.objects.get(user=user_id)
  Wishlist = Wish.objects.filter(user=user_id)
  past_activities = UserActivity.objects.filter(user_id=user_id)
  arr = []
  for activity in past_activities:
    arr.append(Wish.objects.get(id=activity.activity_id))
  return render(request, 'User/wishlist.html', {
    'appuser': appuser,
    'wishlist': Wishlist,
    'acts': arr,
  })

def remove_wish(request, user_id, wish_id):
  wish = Wish.objects.get(id=wish_id)
  wish.delete()
  return redirect('user_wishlist', user_id=user_id)

def activity_to_wish(request, activity_id, user_id):
  activity = Activity.objects.get(id=activity_id)
  if activity in Wish.objects.filter(name=activity.name):
    return redirect('user_wishlist', user_id=user_id)
  else:
    wish = Wish.objects.create(user=AppUser.objects.get(id=user_id), name=activity.name, description=activity.description, interests=[])
    wish.save()
  return redirect('user_wishlist', user_id=user_id)