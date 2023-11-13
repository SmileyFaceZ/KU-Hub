from django.db import models
import datetime
from django.utils import timezone

class Group(models.Model):
    group_name = models.CharField(max_length=200)
    group_member = models.ManyToManyField('auth.User')
    group_tags = models.ManyToManyField('GroupTags')
    group_description = models.CharField(max_length=255)
    create_date = models.DateField(default=datetime.date.today)
    group_password = models.OneToOneField('GroupPassword', on_delete=models.CASCADE, null=True, blank=True)

    def was_published_recently_post(self):
            """
            Checks if the post was published recently.

            Returns:
                bool: True if the post was published within the last day.
            """
            now = timezone.now().date()
            return now - datetime.timedelta(days=1) <= self.create_date <= now

    def __str__(self):
        return self.group_name