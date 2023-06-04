from rest_framework import serializers
import re

# Example regex pattern for alphanumeric password of length 8 to 16 characters
password_regex = r'^[a-zA-Z0-9]{8,16}$'


class PasswordSerializerMixin:
    def validate_password(self, value):
        if not re.match(password_regex, value):
            raise serializers.ValidationError(
                'Password must be alphanumeric and have a length of 8 to 16 characters.', code='invalid_password')
        return value
