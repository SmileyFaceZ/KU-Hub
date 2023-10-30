from django.db import models


class Tags(models.Model):
    tag_text = models.CharField(max_length=200)
