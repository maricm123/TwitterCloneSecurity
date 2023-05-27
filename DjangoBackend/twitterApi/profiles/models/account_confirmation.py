from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    expires_at = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(hours=24))
