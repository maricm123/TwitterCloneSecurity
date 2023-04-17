from rest_framework import serializers
from tweet.models.tweet import Tweet


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['id', 'user', 'text', 'image', 'created_at', 'liked_by']
        read_only_fields = ['id', 'created_at']
