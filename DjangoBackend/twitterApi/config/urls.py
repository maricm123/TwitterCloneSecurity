from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import urls as rest_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("api.urls", namespace="api")),
    path('api-auth/', include('rest_framework.urls')),
]
# urlpatterns += [path("", include(rest_urls, namespace="rest_framework"))]
