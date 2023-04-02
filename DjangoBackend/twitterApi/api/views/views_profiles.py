
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from profiles.models import BusinessUser, DefaultUser, User
from ..serializers.serializers_profiles import BusinessUserSerializer, CustomTokenObtainPairSerializer, DefaultUserSerializer, UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class DefaultUserRegisterView(generics.CreateAPIView):
    """
    View to handle registration of Default Users.
    """
    serializer_class = DefaultUserSerializer


class BusinessUserRegisterView(generics.CreateAPIView):
    """
    View to handle registration of Business Users.
    """
    serializer_class = BusinessUserSerializer



class BusinessUserLoginView(TokenObtainPairView, JWTAuthentication):
    """
    View to handle login of Business Users.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(request.data["email"], "EMAILLLLL")

        print(serializer.validated_data)

        # Get the user_type from the request data
        user_type = serializer.validated_data['user_type']

        if user_type == 'business':
            print(user_type)
            user = User.objects.get(email=request.data["email"])
            user_serializer = UserSerializer(user)
        elif user_type == 'default':
            print(user_type)
            user = User.objects.get(email=request.data["email"])
            user_serializer = UserSerializer(user)
        # else:
        #     return Response({"error": "Invalid user_type"}, status=status.HTTP_400_BAD_REQUEST)

        token_data = serializer.validated_data.copy()
        del token_data['user_type']

        access_token = str(serializer.validated_data['access'])
        response_data = {
            "token": access_token,
            # ovde vratiti business usera mozda
            #  ili jednostavno praviti novi view,  gde cu requestovati business usera
            "user": user_serializer.data,
            "user_type": user_type,
        }
        print(response_data, "RESPONSE DATA")

        return Response(response_data)
