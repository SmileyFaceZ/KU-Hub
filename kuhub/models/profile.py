from django.db import models


class Profile(models.Model):
    """A class represent profile of each user"""
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    biography = models.TextField(blank=True)
    display_photo = models.ImageField(upload_to='media/store/profile_photos/',
                                      null=True,
                                      blank=True,
                                      default='kuhub\static\images\default_profile.jpg')

    def __str__(self):
        return self.user.username
