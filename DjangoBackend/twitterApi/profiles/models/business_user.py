
from .base_profile import BaseProfile
from django.db import models


class BusinessUser(BaseProfile):
    company_name = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)