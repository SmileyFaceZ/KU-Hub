"""Import models from django"""
from django.db import models


class PostDownload(models.Model):
    """
    A class representing downloads of content on the application.

    Attributes:
        post_id(ForeignKey): ID of the post.
        file(FileField): PDF file(s) attached to the post.
        download_data(DateTimeField): Date when the user download file.
        download_count(IntegerField): Counts of downloads for each post.

    """
    post_id = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='downloads'
    )
    file = models.FileField(
        upload_to='store/pdfs/',
        null=True,
        blank=True
    )
    download_date = models.DateTimeField(
        'date downloaded',
        null=True,
        blank=True
    )
    download_count = models.IntegerField(default=0)

    def total_likes(self) -> int:
        """Return the total number of likes for a post."""
        return self.post_id.liked.all().count()

    def total_dislikes(self) -> int:
        """Return the total number of dislikes for a post."""
        return self.post_id.disliked.all().count()

    def like_icon_style(self, user) -> str:
        """Return the style of the like icon when the user clicks the like."""
        if user in self.post_id.liked.all():
            return 'fa-solid fa-thumbs-up'
        else:
            return 'far fa-thumbs-up'

    def dislike_icon_style(self, user) -> str:
        """Return the style of the dislike icon when the user clicks the dislike."""
        if user in self.post_id.disliked.all():
            return 'fa-solid fa-thumbs-down'
        else:
            return 'far fa-thumbs-down'

    def __str__(self) -> str:
        """Return a string with contain the tag, username, and post content."""
        return self.post_id.tag_id.tag_text + ' - ' \
               + str(self.post_id.username) + ' - ' \
               + self.post_id.post_content
