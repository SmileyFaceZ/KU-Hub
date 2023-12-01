from django.http import Http404, HttpRequest
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from kuhub.models import Group, GroupEvent, Note
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404, render
from kuhub.forms import EventForm
from kuhub.calendar import create_event


@method_decorator(login_required, name='dispatch')
class EventDetail(generic.DetailView):
    """Event manage task page view."""
    model = GroupEvent
    template_name = 'kuhub/event_detail.html'

    def get_queryset(self):
        """Get the queryset of all group events."""
        return GroupEvent.objects.all()

    def get_object(self, queryset=None):
        """Get the group event object and check if the current user is a member."""
        obj = super().get_object(queryset)
        is_user_in_group = obj.group.group_member.filter(pk=self.request.user.pk).exists()
        if not is_user_in_group:
            raise Http404("You don't have permission to view this group.")
        return obj

    def get_context_data(self, **kwargs):
        """Get context data for rendering the group event detail page."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['todo'] = self.object.task_set.filter(status='todo')
            context['done'] = self.object.task_set.filter(status='done')
            context['inprogress'] = self.object.task_set.filter(status='in progress')
        return context


def group_event_create(request, group_id):
    """Create a new group event."""
    user = request.user
    is_google_user = user.socialaccount_set.filter(provider='google').exists()
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            meet_link = ''
            group_event = GroupEvent.objects.create(
                group=group,
                summary=data['summary'],
                location=data['location'],
                description=data['description'],
                start_time=data['start_time'].strftime('%Y-%m-%dT%H:%M:%S'),
                end_time=data['end_time'].strftime('%Y-%m-%dT%H:%M:%S'),
                show_time=f"{data['start_time'].strftime('%a. %d %b %Y %H:%M:%S')} - "
                          f"{data['end_time'].strftime('%a. %d %b %Y %H:%M:%S')}"
            )
            if data['is_meeting']:
                try:
                    event, meet_link = create_event(request=request,
                                                    summary=data['summary'],
                                                    description=data['description'],
                                                    location=data['location'],
                                                    start_datetime=data['start_time'].strftime('%Y-%m-%dT%H:%M:%S'),
                                                    end_datetime=data['end_time'].strftime('%Y-%m-%dT%H:%M:%S'))
                except:
                    messages.error(request, "You have to login with google before using this feature")
                    return redirect(reverse('kuhub:group_detail', args=(group_id,)))
            group_event.link = str(meet_link)
            group_event.save()
            messages.success(request, f'create event successful')
            return redirect(reverse('kuhub:group_detail', args=(group_id,)))
    return render(
        request,
        template_name='kuhub/group_event.html',
        context={'form': EventForm, 'group': group, 'user': user, 'is_google': is_google_user}
    )


def group_event_delete(request, event_id):
    """Delete a group event."""
    user = request.user
    event = get_object_or_404(GroupEvent, pk=event_id)
    group_id = event.group.id
    # delete GroupEvent object
    event.delete()
    messages.success(request, 'delete event successful')
    return redirect(reverse('kuhub:group_detail', args=(group_id,)))

