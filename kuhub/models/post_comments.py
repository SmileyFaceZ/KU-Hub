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
    username = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        default=7
    )
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date = models.DateTimeField(
        'date commented', null=True, blank=True
    )

    def __str__(self):
        return self.comment


