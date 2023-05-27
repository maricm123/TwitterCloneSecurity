from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin, Permission
from django.contrib.auth import get_user_model
from .follow_request import FollowRequest


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

    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True)

    follows = models.ManyToManyField(
        'User', blank=True, related_name='followed_by')

    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # used as the unique identifier
    # a list of the field names that will be prompted with createsuperuser
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def unfollow(self, user: get_user_model) -> None:
        """ Helper function to remove a user from this users following list. """
        self.follows.remove(user)

    def follow(self, user: get_user_model, force) -> None:
        """ Helper function to add user to a follower list. """

        if user.id == self.id:
            # ako user sam sebe zapracuje ne radi nista
            return
        # ovde ce mozda drugacije trebati napisati ove casove
        if user.account_status == 'PRIVATE' and force == False:
            FollowRequest.objects.create(
                requester=self, to_follow=user)
        elif user.account_status == 'OPEN' or force == True:
            self.follows.add(user)

    @property
    def following(self) -> models.QuerySet:
        """ Returns a QuerySet of Users that this user follows. """
        return self.follows.all()

    @property
    def followers(self):
        """ Returns a QuerySet of Users following this user. """
        return self.followed_by.all()
