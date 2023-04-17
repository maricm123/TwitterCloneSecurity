
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from profiles.models import BusinessUser, DefaultUser, User
from ..serializers.serializers_profiles import BusinessUserSerializer, CustomTokenObtainPairSerializer, DefaultUserSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status


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


class UserLoginView(TokenObtainPairView, JWTAuthentication):
    """
    View to handle login of Business Users.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the user_type from the request data
        user_type = serializer.validated_data['user_type']

        if user_type == 'business':
            # print(user_type)
            user = User.objects.get(email=request.data["email"])
            user_serializer = UserSerializer(user)
        elif user_type == 'default':
            # print(user_type)
            user = User.objects.get(email=request.data["email"])
            user_serializer = UserSerializer(user)
        else:
            return Response({"error": "Invalid user_type"}, status=status.HTTP_400_BAD_REQUEST)

        token_data = serializer.validated_data.copy()
        del token_data['user_type']

        access_token = str(serializer.validated_data['access'])
        refresh_token = str(serializer.validated_data['refresh'])
        response_data = {
            "token": access_token,
            "refresh": refresh_token,
            # ovde vratiti business usera mozda
            #  ili jednostavno praviti novi view,  gde cu requestovati business usera
            "user": user_serializer.data,
            "user_type": user_type,
        }
        # print(response_data, "RESPONSE DATA")

        return Response(response_data)

# mozemo napraviti opciju za logout sa svih racunara


class LogoutView(APIView):
    # setovanje permisije na view (per-view permision)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MyProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # Retrieve the profile for the current user
        try:
            profile = request.user
            print(profile)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)

        return Response(profile)


class UserProfileView(APIView):
    pass

