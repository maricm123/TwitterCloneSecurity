from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from ..serializers.serializers_tweets import TweetSerializer
from tweet.models.tweet import Tweet


from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class TweetList(generics.ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)


class TweetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # vidi exaplanations ako hoces da dodas neke metode ovde da overidujes - 80


class LikeTweetView(generics.UpdateAPIView):
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()
    http_method_names = ['post', 'delete', 'put']

    def update(self, request, *args, **kwargs):
        tweet = self.get_object()
        print(tweet)
        user = request.user
        print(user)
        if user in tweet.liked_by.all():
            # Korisnik je već lajkao tweet
            return Response({'message': 'Već ste lajkovali ovaj tweet.'}, status=status.HTTP_400_BAD_REQUEST)

        tweet.liked_by.add(user)
        tweet.save()

        serializer = self.get_serializer(tweet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        tweet = self.get_object()
        print(tweet)
        user = request.user
        print(user)
        if user not in tweet.liked_by.all():
            # Korisnik nije lajkao tweet
            return Response({'message': 'Niste lajkovali ovaj tweet.'}, status=status.HTTP_400_BAD_REQUEST)

        tweet.liked_by.remove(user)
        tweet.save()

        serializer = self.get_serializer(tweet)
        return Response(serializer.data, status=status.HTTP_200_OK)
