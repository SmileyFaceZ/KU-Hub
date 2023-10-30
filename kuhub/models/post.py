import datetime

from django.db import models
from django.utils import timezone


class Post(models.Model):
    username = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post_content = models.CharField(max_length=200)
    post_date = models.DateTimeField('date posted', null=True, blank=True)
    post_likes = models.IntegerField(default=0)
    post_dislikes = models.IntegerField(default=0)
    tag_id = models.ForeignKey('Tags', on_delete=models.CASCADE, default=1)

    def was_published_recently_post(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.post_date <= now
