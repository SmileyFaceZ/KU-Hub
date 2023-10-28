from django.db import models
from django.utils import timezone
import datetime

# Create your models here.


class UserFollower(models.Model):
    user_followed = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    follower = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    follow_date = models.DateTimeField('date followed', null=True, blank=True)


class Tags(models.Model):
    tag_text = models.CharField(max_length=200)


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


class PostComments(models.Model):
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    comment_date = models.DateTimeField(
        'date commented', null=True, blank=True
    )


class PostDownload(models.Model):
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    download_date = models.DateTimeField(
        'date downloaded',
        null=True,
        blank=True
    )
    download_count = models.IntegerField(default=0)


class PostReport(models.Model):
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    report_reason = models.CharField(max_length=200)
    report_date = models.DateTimeField('date reported', null=True, blank=True)
    report_count = models.IntegerField(default=0)
