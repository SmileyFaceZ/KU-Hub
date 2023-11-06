"""Import models from django."""
from django.db import models


class PostComments(models.Model):
    """
    A class representing the post's comments

    Attributes:
        post_id(ForeignKey): Represent id of the post.
        comment(CharField): Content of each comment.
        comment_date(DateTimeField): Date that the comment is published.
    """
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    comment_date = models.DateTimeField(
        'date commented', null=True, blank=True
    )
