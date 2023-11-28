"""Import models."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from kuhub.models import Profile
from channels.layers import get_channel_layer


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Signal for creating profile when user is created."""
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Signal yo save profile instance."""
    instance.profile.save()


channel_layer = get_channel_layer()
