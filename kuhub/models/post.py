"""Import datetime, models, timezone from django."""
import datetime

from django.db import models
from django.utils import timezone


class Post(models.Model):
    """
    A class representing a user's post.

    Attributes:
        username (ForeignKey): The user who created the post.
        post_content (CharField): The content of the post.
        post_date (DateTimeField): The date and time when the post was created.
        post_likes (IntegerField): The number of likes received by the post.
        post_dislikes (IntegerField): The number of dislikes received by the post.
        tag_id (ForeignKey): The tag associated with the post.

    Methods:
        was_published_recently_post(): Checks if the post was published recently.

        """
    username = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post_content = models.CharField(max_length=200)
    post_date = models.DateTimeField('date posted', null=True, blank=True)
    post_likes = models.IntegerField(default=0)
    post_dislikes = models.IntegerField(default=0)
    tag_id = models.ForeignKey('Tags', on_delete=models.CASCADE, default=1)

    def was_published_recently_post(self):
        """
        Checks if the post was published recently.

        Returns:
            bool: True if the post was published within the last day.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.post_date <= now
