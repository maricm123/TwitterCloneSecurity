from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin, Permission

class CustomUserManager(BaseUserManager):
    """
    Custom User Manager is required when redefining User class
    """
    def create_user(self,  email, password=None, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(
            password
        )

        user.save()

        return user

    def create_superuser(self,  email, password=None, **extra_fields):
        
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(
    AbstractBaseUser,
    PermissionsMixin
):
    OPEN = "OPEN"
    PRIVATE = "PRIVATE"

    ACCOUNT_STATUS_CHOICES = (
        (OPEN, "open"),
        (PRIVATE, "private"),
    )

    USER_TYPE_CHOICES = [
        ('default', 'Default User'),
        ('business', 'Business User'),
    ]

    email = models.CharField(max_length=80, unique=True)
    username = models.CharField(max_length=45, unique=True)

    account_status = models.CharField(
        choices=ACCOUNT_STATUS_CHOICES,
        default=PRIVATE,
        max_length=512,
        verbose_name=("Account Status"),
    )

    is_staff = models.BooleanField(default=False, verbose_name=("staff"))

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True)

    
    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # used as the unique identifier
    REQUIRED_FIELDS = []  # a list of the field names that will be prompted with createsuperuser

    def __str__(self):
        return self.email
