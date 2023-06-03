import string
import secrets
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def generate_confirmation_token(length=32):
    """
    Generate a random confirmation token of specified length.
    """
    characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(characters) for _ in range(length))
    return token


def generate_reset_token(user):
    token = default_token_generator.make_token(user)

    return token


def generate_uid(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    return uid
