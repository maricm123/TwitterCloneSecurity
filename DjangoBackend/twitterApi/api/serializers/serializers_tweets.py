from rest_framework import serializers
from tweet.models.tweet import Tweet
from .serializers_profiles import UserSerializer


# class UsernameRelatedField(serializers.RelatedField):
#     def to_representation(self, value):
#         return value.username


class TweetSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.email')
    user = UserSerializer(required=False)
    liked_by = serializers.SerializerMethodField()

    def get_liked_by(self, tweet):
        return [user.username for user in tweet.liked_by.all()]

    class Meta:
        model = Tweet
        fields = ['id', 'text', 'image', 'created_at', 'liked_by', 'user']
