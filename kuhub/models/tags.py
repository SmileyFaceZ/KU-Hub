"""Import models from django."""
from django.db import models


class Tags(models.Model):
    """
    Model representing tags for categorizing items.

    Attributes:
        tag_text (str): The text content of the tag.

    """
    tag_text = models.CharField(max_length=200)
