from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from ..serializers.serializers_tweets import TweetSerializer
from tweet.models.tweet import Tweet
from rest_framework.exceptions import PermissionDenied


from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class TweetList(generics.ListCreateAPIView):
    # Dashboard - svi tvitovi i kreiranje tvita
    # Tweet-ove treba sortirati opadajuće prema datumu i vremenu objave.

    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TweetListByUser(generics.ListAPIView):
    # User profile - tvitovi samo od usera
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Tweet.objects.filter(user=user)


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

    # vidi exaplanations ako hoces da dodas neke metode ovde da overidujes - 80


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


class LikedByUsersView(generics.RetrieveAPIView):
    pass
