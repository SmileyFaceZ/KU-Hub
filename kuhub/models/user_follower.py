from django.db import models


class UserFollower(models.Model):
    user_followed = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    follower = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    follow_date = models.DateTimeField('date followed', null=True, blank=True)
