from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    biography = models.TextField(blank=True)
