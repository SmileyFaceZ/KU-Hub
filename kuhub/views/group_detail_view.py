from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from kuhub.forms import EventForm
from kuhub.calendar import create_event, delete_event
from django.views import generic
from kuhub.models import Group, GroupEvent, Note


@method_decorator(login_required, name='dispatch')
class GroupDetail(generic.DetailView):
    """Group manage and detail page."""
    model = Group
    template_name = 'kuhub/group_detail.html'

    def get_queryset(self):
        return Group.objects.all()

    def get_context_data(self, **kwargs):
        """Return user'group data as contect data."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['events'] = self.object.groupevent_set.all()
            context['notes'] = self.object.note_set.all()
        return context


def group_event_create(request,group_id):
    """Create event in group calendar."""
    user = request.user
    group = get_object_or_404(Group,pk=group_id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            event = create_event(
                calendar_id=group.group_calendar,
                 summary=data['summary'],
                 description=data['description'],
                 location=data['location'],
                 attendees=group.group_member.all(),
                 start_datetime=data['start_time']
                                .strftime('%Y-%m-%dT%H:%M:%S'),
                 end_datetime=data['end_time'].strftime('%Y-%m-%dT%H:%M:%S')
            )
            group_event = GroupEvent.objects.create(
                group=group,
                summary=data['summary'],
                location=data['location'],
                description=data['description'],
                start_time=data['start_time']
                            .strftime("%a. %d %b %Y %H:%M:%S"),
                end_time=data['end_time'].strftime("%a. %d %b %Y %H:%M:%S"),
                event_id=event['id']
            )
            # update = generate_meeting(group.group_calendar,group_event)
            messages.success(request, f'create event successful')
            return redirect(
                reverse(
                    'kuhub:group_detail',
                    args=(group_id,)
                )
            )

    return render(
        request,
        template_name='kuhub/group_event.html',
        context={'form': EventForm,'group':group}
    )


def group_event_delete(request,event_id):
    """Delete event in group calendar."""
    user = request.user
    event = get_object_or_404(GroupEvent, pk=event_id)
    group_id = event.group.id
    #delete event in calendar
    delete_event(event.group.group_calendar,event.event_id)
    #delete GroupEvent object
    event.delete()
    messages.success(request,'delete event successful')
    return redirect(reverse('kuhub:group_detail', args=(group_id,)))


def add_note(request,group_id):
    """Add note in group detail page."""
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        text = request.POST.get('note', '')
        Note.objects.create(group=group,note_text=text)
        messages.success(request,'create note successful')
        return redirect(
            reverse(
                'kuhub:group_detail',
                args=(group_id,)
            )
        )


def delete_note(request, note_id):
    """Delete note in group detail page."""
    note = get_object_or_404(Note, pk=note_id)
    group_id = note.group.id
    note.delete()
    messages.success(request,'delete note successful')
    return redirect(reverse('kuhub:group_detail', args=(group_id,)))
