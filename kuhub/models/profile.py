from django.db import models


class Profile(models.Model):
    """
    A class represent profile of each user

     Attributes:
        user (auth.User): OneToOneField to the User model, specifying the user associated with the profile.
        biography (str): Text field for the user's biography.
        display_photo (ImageField): Field for the user's display photo.

    """
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    biography = models.TextField(blank=True)
    display_photo = models.ImageField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username
