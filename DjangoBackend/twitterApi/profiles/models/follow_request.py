from django.db import models
from typing import List, Tuple


class FollowRequest(models.Model):

    requester = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='requester', to_field="email")
    to_follow = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='requests', to_field="email"
    )

    def accept(self) -> None:
        self.requester.follow(self.to_follow, force=True)
        self.delete()

    def reject(self) -> None:
        self.delete()

    def __str__(self):
        return self.to_follow.email

    class Meta:
        indexes: List[models.Index] = [
            models.Index(fields=('to_follow',)),
        ]
