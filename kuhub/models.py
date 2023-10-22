from django.db import models

# Create your models here.


class UserFollower(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    follower = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    folow_date = models.DateTimeField('date followed', null=True, blank=True)


class UserComment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    comment_date = models.DateTimeField(
        'date commented',
        null=True,
        blank=True
    )


class Post(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post_text = models.CharField(max_length=200)
    post_date = models.DateTimeField('date posted', null=True, blank=True)
    post_likes = models.IntegerField(default=0)
    post_unlikes = models.IntegerField(default=0)


class PostComments(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment = models.ForeignKey('UserComment', on_delete=models.CASCADE)


class Tags(models.Model):
    tag_text = models.CharField(max_length=200)


class PostTags(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tags', on_delete=models.CASCADE)


class PostDownload(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    download_date = models.DateTimeField(
        'date downloaded',
        null=True,
        blank=True
    )
    download_count = models.IntegerField(default=0)
