from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import include, path
from .views import (
    views_profiles,
    views_tweets
)
app_name = "api"

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('default-user/login/',views_profiles.DefaultUserLoginView.as_view(), name='default_user_login'),
    path('user/login/', views_profiles.UserLoginView.as_view(), name='user_login'),
    path('default-user/register/', views_profiles.DefaultUserRegisterView.as_view(),
         name='default_user_register'),
    path('business-user/register/', views_profiles.BusinessUserRegisterView.as_view(),
         name='business_user_register'),
    path('current-user/', views_profiles.CurrentUserView.as_view(),
         name='current-user'),

    # logout
    path('logout/', views_profiles.LogoutView.as_view(), name='logout'),
    path('my-profile/<int:pk>/',
         views_profiles.MyProfileView.as_view(), name='my-profile'),

    # tweets
    path('tweet/', views_tweets.TweetList.as_view(), name='tweet'),
    path('tweets-by-me/', views_tweets.TweetListByMe.as_view(), name='tweets-by-me'),
    path('tweets-by-user/<int:pk>/', views_tweets.TweetListByUser.as_view(),
         name='tweets-by-user'),



    path('tweet/<int:pk>/', views_tweets.TweetDetail.as_view(), name='tweet-detail'),
    path('tweet/<int:pk>/like/',
         views_tweets.LikeTweetView.as_view(), name='like_tweet'),


    # follow user
    path('follow-user/<int:pk>/',
         views_profiles.FollowUserAPIView.as_view(), name='follow-user'),
    # accept or reject follow ?
    path('follow-request-action/<int:action>/<int:follow_request_id>/',
         views_profiles.FollowRequestActionView.as_view(), name='follow-request-action'),

    # followers lists
    path('follow-request-list/',
         views_profiles.FollowRequestListView.as_view(), name='follow-request-list'),
    path('do-i-request-list/',
         views_profiles.DoIRequestToFollowListView.as_view(), name='do-i-request-list'),
    # Followers list for logged user and for user
    path('followers-list/<int:user_id>/',
         views_profiles.FollowersListView.as_view(), name='followers-list'),
    path('following-list/<int:user_id>/',
         views_profiles.FollowingListView.as_view(), name='following-list'),
    path('followers-list/',
         views_profiles.FollowersListView.as_view(), name='followers-list'),
    path('following-list/',
         views_profiles.FollowingListView.as_view(), name='following-list'),
]
