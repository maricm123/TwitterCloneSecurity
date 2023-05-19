
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from profiles.models import BusinessUser, DefaultUser, User
from ..serializers.serializers_profiles import BusinessUserSerializer, CustomTokenObtainPairSerializer, FollowersSerializer, FollowRequestSerializer, DefaultUserSerializer, UserSerializer, BusinessUserSerializerForUpdate, DefaultUserSerializerForUpdate
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from profiles.models.follow_request import FollowRequest


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


# DOdati to da samo user koji je ulogovan moze da vidi svoj profil
# dodati ako treba jos neka polja u DefaultUserSerializer
# Napraviti View koji ce da dobija i bussines i default usere ili posebno ili zajedno !!
class MyProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if user.user_type == 'default':
            default_user = DefaultUser.objects.get(user=user)
            serializer = DefaultUserSerializer(default_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if user.user_type == 'business':
            business_user = BusinessUser.objects.get(user=user)
            serializer = BusinessUserSerializer(business_user)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, asd):
        user = self.get_object()

        # Check if the user is the same as the authenticated user
        if user == self.request.user:
            if user.user_type == 'business':
                business_user = BusinessUser.objects.get(
                    user=user)
                # pass request data to the serializer instance
                serializer = BusinessUserSerializerForUpdate(
                    business_user, data=self.request.data)
                serializer.is_valid(raise_exception=True)
                # Ensure data is valid
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif user.user_type == 'default':
                default_user = DefaultUser.objects.get(user=user)
                # pass request data to the serializer instance
                serializer = DefaultUserSerializerForUpdate(
                    default_user, data=self.request.data)
                serializer.is_valid(raise_exception=True)
                # Ensure data is valid
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise ValidationError("Invalid user type")
        else:
            raise PermissionDenied(
                "You do not have permission to update this user.")

# View to get current user on client side


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class FollowUserAPIView(APIView):
    """
    APIView to make a request (or directly follow is user to be followed
    has a public account) by an authenticated user.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        to_follow_id = self.kwargs.get("pk")
        if not to_follow_id:
            return Response(
                {'error': 'Follow request\'s user ID not provided.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_object_or_404(User, id=to_follow_id)
        if user.account_status == "PRIVATE":
            self.request.user.follow(user, force=False)
            return Response({'detail': 'requested'})
        else:
            self.request.user.follow(user, force=True)
            return Response({'detail': 'followed'})


class FollowRequestActionView(APIView):

    """
    APIView to accept or reject a FollowRequest by the person
    who is being requested to act upon said request.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            # action is 1 or 2 from frontend (1 is accepted request, 2 is rejected request)
            action = self.kwargs.get('action')
            follow_request_id = self.kwargs.get('follow_request_id')
        except KeyError as field:
            return Response(
                {'error': f'{str(field)} not provided.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        follow_request: FollowRequest = get_object_or_404(
            FollowRequest, id=follow_request_id
        )

        resp = {'detail': 'rejected'}

        if action == 1:
            print("ACCEPT")
            resp['detail'] = 'accepted'
            follow_request.accept()
        else:
            print("REJECT")
            follow_request.reject()

        return Response(resp)

# /////////////////////////////////////////////////////////////
#
#
#
#
#
# LISTE USERA KOJE PRATIMO KOJI NAS PRATE I REQUEST ZA PRACENJE


class FollowRequestListView(generics.ListAPIView):
    # ovo je view samo za ulogovanog korisnika, treba napraviti isti ovakav view samo za usera koji se trazi (iz url-a)
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowRequestSerializer

    #  koristiti metode tj querysetove koji su napisani u user modelu, umesto ovog dole sto sam pisao
    def get_queryset(self):
        print(self.request.user.requests.all(), "REQUESTS")
        # ovo je lista zahteva za pracenje
        return self.request.user.requests.all()

# Da li ja hocu da pratim nekoga? da li requestujem da pratim nekog


class DoIRequestToFollowListView(generics.ListAPIView):
    # ovo je view samo za ulogovanog korisnika, treba napraviti isti ovakav view samo za usera koji se trazi (iz url-a)
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowRequestSerializer

    #  koristiti metode tj querysetove koji su napisani u user modelu, umesto ovog dole sto sam pisao
    def get_queryset(self):
        print(self.request.user.requester.all(), "REQUESTER")
        # ovo je lista zahteva za pracenje
        return self.request.user.requester.all()


class FollowersListView(generics.ListAPIView):
    # ovo je view samo za ulogovanog korisnika, treba napraviti isti ovakav view samo za usera koji se trazi (iz url-a)
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowersSerializer

    #  koristiti metode tj querysetove koji su napisani u user modelu, umesto ovog dole sto sam pisao
    def get_queryset(self):
        # ovo je lista usera koji prate mene (tj usera koji je pozvao ovo)
        # get the user_id from the URL parameter, if provided
        user = self.kwargs.get('user_id', None)
        if user:
            return get_object_or_404(User, id=user).followers.all()
        else:
            return self.request.user.followers.all()


class FollowingListView(generics.ListAPIView):
    # ovo je view samo za ulogovanog korisnika, treba napraviti isti ovakav view samo za usera koji se trazi (iz url-a)
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowersSerializer

    #  koristiti metode tj querysetove koji su napisani u user modelu, umesto ovog dole sto sam pisao
    def get_queryset(self):
        # ovo je lista usera koji prate mene (tj usera koji je pozvao ovo)
        # print(self.request.user.followed_by.all())
        # ovo je lista usera koje ja pratim

        # ovo je lista zahteva za pracenje
        # print(self.request.user.requests.all())
        return self.request.user.follows.all()
