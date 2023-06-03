
from profiles.models.account_confirmation import AccountConfirmation
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from profiles.models import BusinessUser, DefaultUser, User, AccountConfirmation
from ..serializers.serializers_profiles import (
    BusinessUserSerializer,
    CustomTokenObtainPairSerializer,
    FollowersSerializer,
    FollowRequestSerializer,
    DefaultUserSerializer,
    UserSerializer,
    BusinessUserSerializerForUpdate,
    DefaultUserSerializerForRegister,
    BusinessUserSerializerForRegister
)
from django.utils import timezone

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from profiles.models.follow_request import FollowRequest
from ..utils import generate_confirmation_token, generate_reset_token, generate_uid
from django.contrib.auth.tokens import default_token_generator

from django.utils.http import urlsafe_base64_decode


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# def generate_confirmation_token(length=32):
#     """
#     Generate a random confirmation token of specified length.
#     """
#     characters = string.ascii_letters + string.digits
#     token = ''.join(secrets.choice(characters) for _ in range(length))
#     return token


# {
#     "token" : "hRVEcGwmmkZ9AhnWTslrAqnfq7axRQ4D"
# }
class AccountConfirmationVerifyView(APIView):
    def post(self, request):
        token = request.data.get('token')
        # Pronalaženje potvrde naloga na osnovu tokena
        try:
            confirmation = AccountConfirmation.objects.get(token=token)
        except AccountConfirmation.DoesNotExist:
            return Response({'error': 'Neispravan token potvrde naloga'}, status=status.HTTP_400_BAD_REQUEST)

        # Provera da li je potvrda naloga istekla
        if confirmation.expires_at < timezone.now():
            return Response({'error': 'Token potvrde naloga je istekao'}, status=status.HTTP_400_BAD_REQUEST)

        # Potvrda naloga
        user = confirmation.user
        user.is_active = True
        user.save()
        # Brisanje potvrde naloga iz baze podataka
        confirmation.delete()

        return Response({'message': 'Nalog je uspešno potvrđen'}, status=status.HTTP_200_OK)


class DefaultUserRegisterView(generics.CreateAPIView):
    """
    View to handle registration of Default Users.
    """
    serializer_class = DefaultUserSerializerForRegister

    def perform_create(self, serializer):
        # Call the default perform_create() method to handle user registration
        user = serializer.save()

        # Generate confirmation token
        token = generate_confirmation_token()

        # Create account confirmation
        confirmation = AccountConfirmation.objects.create(
            user=user.user, token=token)

        # Send confirmation email
        # Replace the following code with your email sending logic
        # email_subject = 'Account Confirmation'
        # Include the token in the email
        # email_message = f'Confirmation token: {token}'
        # send_email(user.email, email_subject, email_message)

        # Return a response indicating successful registration
        return Response({'message': 'User registered successfully. Please check your email for confirmation.'})


class BusinessUserRegisterView(generics.CreateAPIView):
    """
    View to handle registration of Business Users.
    """
    serializer_class = BusinessUserSerializerForRegister

    def perform_create(self, serializer):
        # Call the default perform_create() method to handle user registration
        user = serializer.save()

        # Generate confirmation token
        token = generate_confirmation_token()

        # Create account confirmation
        confirmation = AccountConfirmation.objects.create(
            user=user.user, token=token)

        # Send confirmation email
        # Replace the following code with your email sending logic
        # email_subject = 'Account Confirmation'
        # Include the token in the email
        # email_message = f'Confirmation token: {token}'
        # send_email(user.email, email_subject, email_message)

        # Return a response indicating successful registration
        return Response({'message': 'User registered successfully. Please check your email for confirmation.'})


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
            user = User.objects.get(email=request.data["email"])
            user_serializer = UserSerializer(user)
        elif user_type == 'default':
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

    def get_queryset(self):
        # ovo je lista zahteva za pracenje
        return self.request.user.requests.all()

# Da li ja hocu da pratim nekoga? da li requestujem da pratim nekog


class DoIRequestToFollowListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowRequestSerializer

    def get_queryset(self):
        # ovo je lista zahteva za pracenje
        return self.request.user.requester.all()


class FollowersListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowersSerializer

    def get_queryset(self):
        user = self.kwargs.get('user_id', None)
        if user:
            return get_object_or_404(User, id=user).followers.all()
        else:
            return self.request.user.followers.all()


class FollowingListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowersSerializer

    def get_queryset(self):
        user = self.kwargs.get('user_id', None)
        if user:
            return get_object_or_404(User, id=user).follows.all()
        else:
            return self.request.user.follows.all()


# View gde korisnik unosi mail i na njegov mail se salje link gde ce resetovti lozinnku
class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return Response({'error': 'There is no user with this mail'}, status=400)

        token = generate_reset_token(user)
        uid = generate_uid(user)
        # Slanje e-pošte sa linkom za resetovanje lozinke
        reset_password_url = f' http://localhost:8080/reset-password/{uid}/{token}'
        print(reset_password_url)
        # send_mail(
        #     'Resetovanje lozinke',
        #     f'Molimo posetite sledeći link da biste resetovali lozinku: {reset_password_url}',
        #     'noreply@example.com',
        #     [email],
        #     fail_silently=False,
        # )

        return Response({'success': 'Email with confirmation message was sent.'})


class ResetPasswordConfirmView(APIView):
    def post(self, request):
        token = request.data.get('token')
        uid = request.data.get('uid')

        try:
            user_id = urlsafe_base64_decode(uid)
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Neispravan link za resetovanje lozinke.'}, status=400)

        if default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')

            # Validacija i ažuriranje nove lozinke
            user.set_password(new_password)
            user.save()

            return Response({'success': 'Lozinka je uspešno resetovana.'})

        return Response({'error': 'Neispravan link za resetovanje lozinke.'}, status=400)
