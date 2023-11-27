from django.db import models


class Profile(models.Model):
    """A class represent profile of each user"""
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    biography = models.TextField(blank=True)
    display_photo = models.ImageField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username
