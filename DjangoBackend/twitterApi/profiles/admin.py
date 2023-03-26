from django.contrib import admin
# from .models import User
from django.contrib.auth import get_user_model
from profiles.models.base_profile import BaseProfile
from profiles.models.default_user import DefaultUser
from profiles.models.business_user import BusinessUser

# Register your models here.

User = get_user_model()

admin.site.register(User)
admin.site.register(DefaultUser)
admin.site.register(BusinessUser)