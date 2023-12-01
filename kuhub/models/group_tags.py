"""Import models from django."""
from django.db import models


class GroupTags(models.Model):
    """
        Model representing tags associated with groups in Group Hub.

        Attributes:
            tag_text (str): The text representing the tag.
    """
    tag_text = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_text