"""Import models from django."""
from django.db import models


class Tag(models.Model):
    """Class Tag table."""
    tag_text = models.CharField(max_length=200)
