"""Import models from django."""
from django.db import models


class Tags(models.Model):
    """Class Tags table."""
    tag_text = models.CharField(max_length=200)
