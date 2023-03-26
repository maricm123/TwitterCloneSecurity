from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import include, path
from .views import (
    views_profiles 
)
app_name = "api"

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('default-user/login/',views_profiles.DefaultUserLoginView.as_view(), name='default_user_login'),
    path('business-user/login/', views_profiles.BusinessUserLoginView.as_view(), name='business_user_login'),
    path('default-user/register/', views_profiles.DefaultUserRegisterView.as_view(), name='default_user_register'),
    path('business-user/register/', views_profiles.BusinessUserRegisterView.as_view(), name='business_user_register'),
]
