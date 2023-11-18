from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from kuhub.models import Profile, Notification, PostReport, PostComments
from channels.layers import get_channel_layer


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


channel_layer = get_channel_layer()


@receiver(post_save, sender=PostReport)
def post_report_notification(sender, instance, **kwargs):
    # Send notification when a post is reported
    group_name = f"post_{instance.post_id.id}_notifications"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'post_report_notification',
            'message': 'A post has been reported!',
        }
    )


@receiver(post_save, sender=PostComments)
def comment_notification(sender, instance, **kwargs):
    # Send notification when a comment is added
    group_name = f"post_{instance.post_id.id}_notifications"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'comment_notification',
            'message': 'A new comment has been added!',
        }
    )
