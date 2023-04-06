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
    path('user/<int:user_id>/interests/edit/', views.interests_edit, name='edit_interest'),

    path('user/<int:user_id>/interests/add/<str:interest>/', views.interests_add, name='add_interest'),
    path('user/<int:user_id>/interests/remove/<str:interest>/', views.interests_remove, name='remove_interest'),

    path('user/<int:user_id>/create/', views.UserCreate.as_view(), name='create_appuser'),
    # recommend path
        # this is the path to the recommendation page
    path('user/<int:user_id>/recommend/', views.recommend, name='recommend'),

    path('user/<int:user_id>/recommend/<int:activity_id>/', views.add_activity, name='add_activity'),

    path('user/<int:user_id>/wishlist', views.user_wishlist, name='user_wishlist'),

    path('user/<int:user_id>/wishlist/<str:activity_str>/', views.add_wishlist, name='add_wishlist'),

    path('user/<int:user_id>/wish/delete/<int:wish_id>', views.remove_wish, name='remove_wish'),

    path('accounts/', include('django.contrib.auth.urls')),
        # localhost:8000/accounts/login 
        # built in django user authentication
    # path('user/<int:user_id>/past_activities/', views.past_activities.as_view(), name='past_activities'),
    path('accounts/signup/', views.signup, name='signup'),

    #activity paths
    path('activity/redirect/<str:wish_str>/', views.activity_deets, name='activity_redirect'),
    path('activity/', views.ActivityList.as_view(), name='activity'),
    path('activity/<int:pk>/', views.ActivityDetail.as_view(), name='activity_detail'),
    path('activity/create/', views.ActivityCreate.as_view(), name='activity_create'),
    path('activity/<int:pk>/update/', views.ActivityUpdate.as_view(), name='activity_update'),
    path('activity/<int:pk>/delete/', views.ActivityDelete.as_view(), name='activity_delete'),
    
    path('ai_rec/<int:user_id>', views.ai_rec, name='ai_rec')
]