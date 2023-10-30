from django.db import models


class PostDownload(models.Model):
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='downloads')
    download_date = models.DateTimeField(
        'date downloaded',
        null=True,
        blank=True
    )
    download_count = models.IntegerField(default=0)