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
