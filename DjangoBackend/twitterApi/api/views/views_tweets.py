from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from ..serializers.serializers_tweets import TweetSerializer
from tweet.models.tweet import Tweet
from profiles.models.user import User
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

"""
Home feed treba da sadrži listu tweet-ova tog korisnika
i svih ostalih korisnika koje taj profil prati.
"""


class TweetList(generics.ListCreateAPIView):
    # Dashboard - svi tvitovi i kreiranje tvita
    # Tweet-ove treba sortirati opadajuće prema datumu i vremenu objave.

    queryset = Tweet.objects.order_by('-created_at')
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TweetListDashboard(generics.ListAPIView):
    serializer_class = TweetSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        followers = user.following
        follower_ids = list(followers.values_list('id', flat=True)) + [user.id]
        return Tweet.objects.filter(user__in=follower_ids).order_by('-created_at')


class TweetListByMe(generics.ListAPIView):
    # User profile - tvitovi samo od usera koji je ulogovan
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Tweet.objects.filter(user=user).order_by('-created_at')


class TweetListByUser(generics.ListAPIView):
    # User profile - tvitovi samo od usera
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the user ID from the URL parameter
        user_id = self.kwargs.get('pk')
        # Retrieve the user object from the database
        user = get_object_or_404(User, id=user_id)
        return Tweet.objects.filter(user=user).order_by('-created_at')


class TweetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        tweet = self.get_object()
        if tweet.user == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied(
                "You do not have permission to update this tweet.")

    def perform_destroy(self, instance):
        tweet = self.get_object()
        if tweet.user == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied(
                "You do not have permission to delete this tweet.")


class LikeTweetView(generics.UpdateAPIView):
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['post', 'delete', 'put']

    def update(self, request, *args, **kwargs):
        tweet = self.get_object()
        user = self.request.user

        tweet.liked_by.add(user)
        tweet.save()

        serializer = self.get_serializer(tweet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        tweet = self.get_object()
        user = self.request.user

        tweet.liked_by.remove(user)
        tweet.save()

        serializer = self.get_serializer(tweet)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetweetView(generics.ListCreateAPIView):
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        tweet_id = self.kwargs.get("pk")
        original_tweet = get_object_or_404(Tweet, id=tweet_id)
        user_follows = user.follows.filter(id=original_tweet.user.id).exists()
        print(user_follows)
        # Provera pristupa originalnom tweet-u
        # Ako je originalni tweet privatna objava i korisnik ne prati autora ili hoce da retweetuje svoj tweet, vraćamo zabranu pristupa
        if (original_tweet.user.account_status == "PRIVATE" and user_follows == False) or user.id == original_tweet.user.id:
            return Response({"detail": "Nemate pristup ovom tweet-u."}, status=status.HTTP_403_FORBIDDEN)

        # Kreiranje retweet-a
        retweet = Tweet.objects.create(
            text=original_tweet.text,
            user=user,
            original_tweet=original_tweet,
            is_retweet=True
        )

        serializer = TweetSerializer(
            retweet, context={'original_tweet_user': original_tweet.user.id})
        serializer_data = serializer.data
        serializer_data['original_tweet_user'] = serializer.context['original_tweet_user']
        print(serializer_data)
        return Response(serializer_data, status=status.HTTP_201_CREATED)
