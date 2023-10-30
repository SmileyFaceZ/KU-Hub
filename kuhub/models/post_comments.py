from django.db import models


class PostComments(models.Model):
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    comment_date = models.DateTimeField(
        'date commented', null=True, blank=True
    )