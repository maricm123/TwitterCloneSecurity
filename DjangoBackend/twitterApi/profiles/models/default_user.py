from .base_profile import BaseProfile
from django.db import models


class DefaultUser(BaseProfile):
    first_name = models.CharField(max_length=30, blank=True, verbose_name=("first name"))
    last_name = models.CharField(max_length=30, blank=True, verbose_name=("last name"))
    age = models.IntegerField()
    address = models.CharField(max_length=50, null=True, blank=True)