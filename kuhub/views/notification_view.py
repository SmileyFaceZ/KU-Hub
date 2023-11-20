from django.views import generic
from kuhub.models import Notification


class NotificationView(generic.ListView):
    """Redirect users to notification page and show list of notification"""
    template_name = 'kuhub/notification.html'
    context_object_name = 'notifications_list'

    def get_queryset(self):
        return (Notification.objects
                .filter(user=self.request.user)
                .order_by("-id"))
