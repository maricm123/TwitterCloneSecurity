from rest_framework import serializers
from tweet.models.tweet import Tweet
from .serializers_profiles import UserSerializer


class TweetSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.email')
    user = UserSerializer()

    class Meta:
        model = Tweet
        fields = ['id', 'text', 'image', 'created_at', 'liked_by', 'user']
