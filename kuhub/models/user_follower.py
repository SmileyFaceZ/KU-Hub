"""Import models from django."""
from django.db import models


class UserFollower(models.Model):
    """
    A class representing a user following and follower

    Attributes:
        user_followed(auth.User): Users that the user follows.
        follower(auth.User): Users following the user.
        follow_date(DateTime): A date when the user follow others.
    """
    user_followed = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    follower = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    follow_date = models.DateTimeField('date followed', null=True, blank=True)
