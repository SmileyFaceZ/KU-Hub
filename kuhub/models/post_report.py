"""import models from django"""
from django.db import models


class PostReport(models.Model):
    """
    A class represent report of posts

    Attributes:
        post_id(ForeignKey): ID of the post.
        report_reason(CharField): Reason of the report.
        report_date(DateTimeField): Date when a user report the post.
        report_count(IntegerField): Report count of the post.
    """
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    report_reason = models.CharField(max_length=200)
    report_date = models.DateTimeField('date reported', null=True, blank=True)
    report_count = models.IntegerField(default=0)

    def __str__(self):
        """Return reason of reporting post."""
        return self.report_reason
