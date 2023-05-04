from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tweet(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='tweets/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(
        User, related_name='liked_tweets', blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tweets')

    def __str__(self):
        return self.text
