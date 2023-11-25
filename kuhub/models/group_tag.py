"""Import models from django."""
from django.db import models


class GroupTag(models.Model):
    """Class Tag table."""
    tag_text = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_text
