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

    # logout
    path('logout/', views_profiles.LogoutView.as_view(), name='logout'),
    path('my-profile/', views_profiles.MyProfileView.as_view(), name='my-profile'),
    path('user-profile/', views_profiles.UserProfileView.as_view(), name='my-profile'),

    # tweets
    path('tweet/', views_tweets.TweetList.as_view(), name='tweet'),
    path('tweets-by-me/', views_tweets.TweetListByUser.as_view(), name='tweets-by-me'),
    path('tweet/<int:pk>/', views_tweets.TweetDetail.as_view(), name='tweet-detail'),
    path('tweet/<int:pk>/like/',
         views_tweets.LikeTweetView.as_view(), name='like_tweet'),
]
