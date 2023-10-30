from django.db import models


class PostReport(models.Model):
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    report_reason = models.CharField(max_length=200)
    report_date = models.DateTimeField('date reported', null=True, blank=True)
    report_count = models.IntegerField(default=0)
