
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from profiles.models import BusinessUser, DefaultUser
from ..serializers.serializers_profiles import BusinessUserSerializer, CustomTokenObtainPairSerializer, DefaultUserSerializer

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


# class DefaultUserLoginView(TokenObtainPairView):
#     """
#     View to handle login of Default Users.
#     """
#     serializer_class = CustomTokenObtainPairSerializer

# class BusinessUserLoginView(TokenObtainPairView):
#     """
#     View to handle login of Business Users.
#     """
#     serializer_class = CustomTokenObtainPairSerializer







class DefaultUserLoginView(TokenObtainPairView):
    """
    View to handle login of Default Users.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the user_type from the request data
        user_type = serializer.validated_data['user_type']

        if user_type == 'default':
            # user = DefaultUser.objects.get(username=serializer.validated_data['username'])
            # user_serializer = DefaultUserSerializer(user)
            user_serializer = DefaultUserSerializer()
        else:
            return Response({"error": "Invalid user_type"}, status=status.HTTP_400_BAD_REQUEST)

        token_data = serializer.validated_data.copy()
        print(token_data)
        del token_data['user_type']
        # del token_data['password']

        response_data = {
            "token": serializer.get_token().access_token,
            "user": user_serializer.data,
            "user_type": user_type,
        }
        print(response_data)

        return Response(response_data)

class BusinessUserLoginView(TokenObtainPairView):
    """
    View to handle login of Business Users.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(serializer.validated_data)

        # Get the user_type from the request data
        user_type = serializer.validated_data['user_type']

        if user_type == 'business':
            
            user_serializer = DefaultUserSerializer(user)
        else:
            return Response({"error": "Invalid user_type"}, status=status.HTTP_400_BAD_REQUEST)

        token_data = serializer.validated_data.copy()
        del token_data['user_type']
        del token_data['password']

        response_data = {
            "token": serializer.get_token(user).access_token,
            "user": user_serializer.data,
            "user_type": user_type,
        }

        return Response(response_data)