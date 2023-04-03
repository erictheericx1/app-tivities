from django.urls import path, include
from . import views

urlpatterns = [
    # home paths
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # user paths
        # for now when you look at user it starts off showing past activities
    path('user/', views.UserCreate.as_view(), name='user'),
    path('user/<int:user_id>/', views.past_activities, name='past_activities'),
        # this is the path to the user's interests
    path('user/<int:user_id>/interests/', views.interests, name='interests'),
        # bcs interests is an array of the user, we just need to update the user model
    path('user/<int:user_id>/interests/edit/', views.UserUpdate.as_view(), name='edit_interest'),
    # recommend path
        # this is the path to the recommendation page
    path('user/<int:user_id>/recommend/', views.recommend, name='recommend'),
    path('accounts/', include('django.contrib.auth.urls'))
        # localhost:8000/accounts/login 
        # built in django user authentication
]

