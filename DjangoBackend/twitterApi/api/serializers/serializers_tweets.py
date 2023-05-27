from rest_framework import serializers
from tweet.models.tweet import Tweet
from .serializers_profiles import UserSerializer


class TweetSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.email')
    user = UserSerializer(required=False)
    liked_by = serializers.SerializerMethodField()
    original_tweet_user = serializers.SerializerMethodField()

    def get_liked_by(self, tweet):
        return [user.username for user in tweet.liked_by.all()]

    def get_original_tweet_user(self, tweet):
        pass

    class Meta:
        model = Tweet
        fields = ['id', 'text', 'image', 'created_at',
                  'liked_by', 'user', 'original_tweet', 'is_retweet', 'original_tweet_user',]
