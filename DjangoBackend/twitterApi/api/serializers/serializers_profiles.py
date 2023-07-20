from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from profiles.models.business_user import BusinessUser
from profiles.models.default_user import DefaultUser
from profiles.models.follow_request import FollowRequest
from rest_framework.validators import UniqueValidator
from ..mixins import PasswordSerializerMixin

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Overrides the default TokenObtainPairSerializer to return the user_type in the token response.
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        access = refresh.access_token
        data['user_type'] = self.user.user_type
        data['refresh'] = str(refresh)
        data['access'] = str(access)
        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the base User model.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',
                  'user_type', 'account_status', 'follows', 'address',)
        read_only_fields = ('id', 'user_type', 'follows',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class DefaultUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the Default User model. Inherits the base User serializer.
    """
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(write_only=True, source='user.password')
    email = serializers.CharField(source='user.email', validators=[
                                  UniqueValidator(queryset=User.objects.all())])
    user_type = serializers.CharField(source='user.user_type')
    account_status = serializers.CharField(source='user.account_status')
    follows = serializers.CharField(source='user.follows')
    address = serializers.CharField(source='user.address')

    class Meta:
        model = DefaultUser
        fields = ('id', 'username', 'password',
                  'email', 'first_name', 'last_name', 'age', 'address', 'user_type', 'account_status', "follows", 'address',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_type = user_data.pop('user_type', 'default')
        user = User.objects.create_user(**user_data, user_type=user_type)
        default_user = DefaultUser.objects.create(user=user, **validated_data)

        return default_user


class DefaultUserSerializerForRegister(serializers.ModelSerializer, PasswordSerializerMixin):
    """
    Serializer for the Default User model. Inherits the base User serializer.
    """
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(write_only=True, source='user.password')
    email = serializers.CharField(source='user.email', validators=[
                                  UniqueValidator(queryset=User.objects.all())])
    user_type = serializers.CharField(source='user.user_type')
    address = serializers.CharField(source='user.address')

    class Meta:
        model = DefaultUser
        fields = ('id', 'username', 'password',
                  'email', 'first_name', 'last_name', 'age', 'address', 'user_type', 'address',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_type = user_data.pop('user_type', 'default')
        user = User.objects.create_user(**user_data, user_type=user_type)
        default_user = DefaultUser.objects.create(user=user, **validated_data)

        return default_user


class BusinessUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the Business User model. Inherits the base User serializer.
    """

    username = serializers.CharField(source='user.username')
    password = serializers.CharField(write_only=True, source='user.password')
    email = serializers.CharField(source='user.email', validators=[
                                  UniqueValidator(queryset=User.objects.all())])
    user_type = serializers.CharField(source='user.user_type')
    account_status = serializers.CharField(source='user.account_status')
    follows = serializers.CharField(source="user.follows")
    address = serializers.CharField(source='user.address')

    class Meta:
        model = BusinessUser
        fields = ('id', 'username', 'password', 'user_type',
                  'email',  'account_status', 'company_name', 'website', "follows", 'address',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_type = user_data.pop('user_type', 'business')
        user = User.objects.create_user(**user_data, user_type=user_type)
        business_user = BusinessUser.objects.create(
            user=user, **validated_data)

        return business_user


class BusinessUserSerializerForRegister(serializers.ModelSerializer, PasswordSerializerMixin):
    """
    Serializer for the Business User model. Inherits the base User serializer.
    """

    username = serializers.CharField(source='user.username')
    password = serializers.CharField(write_only=True, source='user.password')
    email = serializers.CharField(source='user.email', validators=[
                                  UniqueValidator(queryset=User.objects.all())])
    user_type = serializers.CharField(source='user.user_type')
    address = serializers.CharField(source='user.address')

    class Meta:
        model = BusinessUser
        fields = ('id', 'username', 'password', 'user_type',
                  'email', 'company_name', 'website', 'address')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_type = user_data.pop('user_type', 'business')
        user = User.objects.create_user(**user_data, user_type=user_type)
        business_user = BusinessUser.objects.create(
            user=user, **validated_data)

        return business_user


class BusinessUserSerializerForUpdate(serializers.ModelSerializer):
    """
    Serializer for the Business User model. Inherits the base User serializer.
    """
    from rest_framework.validators import UniqueValidator

    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    account_status = serializers.CharField(source='user.account_status')

    class Meta:
        model = BusinessUser
        fields = ('id', 'username',
                  'email',  'account_status', 'company_name', 'website',)
        # fields = ('id', 'user', 'company_name', 'website')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_type = user_data.pop('user_type', 'business')
        user = User.objects.create_user(**user_data, user_type=user_type)
        business_user = BusinessUser.objects.create(
            user=user, **validated_data)

        return business_user

    def update(self, instance, validated_data):
        # Update the related User object
        user_data = validated_data.pop('user', {})
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update the BusinessUser object
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class DefaultUserSerializerForUpdate(serializers.ModelSerializer):
    """
    Serializer for the Default User model. Inherits the base User serializer.
    """
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    user_type = serializers.CharField(source='user.user_type')
    account_status = serializers.CharField(source='user.account_status')

    class Meta:
        model = DefaultUser
        fields = ('id', 'username',
                  'email', 'first_name', 'last_name', 'age', 'address', 'user_type', 'account_status',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_type = user_data.pop('user_type', 'default')
        user = User.objects.create_user(**user_data, user_type=user_type)
        default_user = DefaultUser.objects.create(user=user, **validated_data)

        return default_user

    def update(self, instance, validated_data):
        # Update the related User object
        user_data = validated_data.pop('user', {})
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update the BusinessUser object
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class FollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRequest
        fields = '__all__'


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
