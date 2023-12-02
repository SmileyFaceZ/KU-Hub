"""This module for manage event detail information group."""
from django.utils.decorators import method_decorator
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.views import generic
from kuhub.models import GroupEvent


@method_decorator(login_required, name='dispatch')
class EventDetail(generic.DetailView):
    """Group manage and detail page."""

    model = GroupEvent
    template_name = 'kuhub/event_detail.html'

    def get_queryset(self):
        """Retrieve all group event objects from the database."""
        return GroupEvent.objects.all()

    def get_object(self, queryset=None):
        """Retrieve the specific group event object based on the query."""
        obj = super().get_object(queryset)
        is_user_in_group = obj.group.group_member.filter(
            pk=self.request.user.pk).exists()
        if not is_user_in_group:
            raise Http404("You don't have permission to view this group.")
        return obj

    def get_context_data(self, **kwargs):
        """Return user'group data as contect data."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['todo'] = self.object.task_set.filter(status='todo')
            context['done'] = self.object.task_set.filter(status='done')
            context['inprogress'] = self.object.task_set.filter(
                status='in progress')
        return context
