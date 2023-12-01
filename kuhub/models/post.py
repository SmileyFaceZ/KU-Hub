"""Import datetime, models, timezone from django."""
import datetime

from django.db import models
from django.utils import timezone


class Post(models.Model):
    """
    A class representing a user's post.

    Attributes:
        username (auth.User): The user who created the post.
        post_content (str): The content of the post.
        post_date (DateTime): The date and time when the post was created.
        liked (QuerySet): The number of likes the post.
        disliked (QuerySet): The number of dislikes the post.
        tag_id (Tags): The tag associated with the post.
        subject_id (Subject): The subject associated with the post.
        """
    username = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )
    post_content = models.CharField(max_length=200)
    post_date = models.DateTimeField(
        'date posted',
        null=True,
        blank=True
    )
    liked = models.ManyToManyField(
        'auth.User',
        blank=True,
        related_name='likes'
    )
    disliked = models.ManyToManyField(
        'auth.User',
        blank=True,
        related_name='dislikes'
    )
    tag_id = models.ForeignKey(
        'Tags',
        on_delete=models.CASCADE,
        default=1
    )
    subject = models.ForeignKey(
        'Subject',
        on_delete=models.CASCADE,
        blank=True,
        default=1
    )

    def was_published_recently_post(self) -> bool:
        """
        Checks if the post was published recently.

        Returns:
            bool: True if the post was published within the last day.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.post_date <= now

    def total_likes(self) -> int:
        """Return the total number of likes for a post."""
        return self.liked.all().count()

    def total_dislikes(self) -> int:
        """Return the total number of dislikes for a post."""
        return self.disliked.all().count()

    def like_icon_style(self, user) -> str:
        """Return the style of the like icon when the user clicks the like."""
        if user in self.liked.all():
            return 'fa-solid fa-thumbs-up'
        else:
            return 'far fa-thumbs-up'

    def dislike_icon_style(self, user) -> str:
        """Return the style of the dislike icon when the user clicks the dislike."""
        if user in self.disliked.all():
            return 'fa-solid fa-thumbs-down'
        else:
            return 'far fa-thumbs-down'

    def __str__(self) -> str:
        """Return a string with contain the tag, username, and post content."""
        return self.tag_id.tag_text + ' - ' \
               + str(self.username) + ' - ' \
               + self.post_content
