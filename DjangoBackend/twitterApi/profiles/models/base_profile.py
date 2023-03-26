from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils.functional import cached_property

User = get_user_model()


class BaseProfile(models.Model):
    """
    Used to extend all profiles (Convive / TeamMember) given them tools
    NOTE: only to be used with profiles model, or will create an error.
    """

    class Meta:
        abstract = True

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name} ({self.email})"

    @cached_property
    def as_app_log(self):  # override as_app_log() from AppLogFormatable
        return f"{self.name} ({self.pk})"

    @cached_property
    def name(self):
        return self.user.username

    @cached_property
    def name_hidden_last(self):
        return self.user.name_hidden_last

    @cached_property
    def email(self):
        return self.user.email

    @cached_property
    def phone_number(self):
        return self.user.phone_number

    def get_drf_token(self, password):
        """Get DRF authentication token if password is OK"""
        return self.user.get_drf_token(password)

    @transaction.atomic
    def delete(self, force_policy=None, **kwargs):
        """Emulate cascade behaviour"""

        super().delete(force_policy, **kwargs)

    @transaction.atomic
    def undelete(self, force_policy=None, **kwargs):
        """Emulate cascade behaviour"""

        # Undeletes user related to the profile
        if hasattr(self, "user"):
            self.user.undelete()

        super().undelete(force_policy, **kwargs)

    @classmethod
    @transaction.atomic
    def create(cls, user_kwargs=None, profile_kwargs=None):
        """
        Wrapper to create a profile and a user at once
        NOTE: dicts kwargs are None instead of {} to avoid unexpected behaviour.
        But to call them with empty values, use {}, not None.
        """

        new_user = User.objects.create_user(**user_kwargs)
        return cls.objects.create(user=new_user, **profile_kwargs)
