from django.http import Http404
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from kuhub.models import Group, Note
from django.contrib import messages
from kuhub.filters import TaskFilter
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404, render


@method_decorator(login_required, name='dispatch')
class GroupDetail(generic.DetailView):
    """View for managing and displaying details of a group."""
    model = Group
    template_name = 'kuhub/group_detail.html'

    def get_queryset(self):
        """Get the queryset of all groups."""
        return Group.objects.all()

    def get_object(self, queryset=None):
        """Get the group object and check if the current user is a member."""
        obj = super().get_object(queryset)
        is_user_in_group = obj.group_member.filter(pk=self.request.user.pk).exists()
        if not is_user_in_group:
            raise Http404("You don't have permission to view this group.")
        return obj

    def get_filter_set(self):
        """Get the task filter set for the group."""
        return TaskFilter(self.request.GET, queryset=self.object.task_set.all())

    def get_context_data(self, **kwargs):
        """Get context data for rendering the group detail page."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['events'] = self.object.groupevent_set.all()
            context['notes'] = self.object.note_set.all()
            context['filter'] = self.get_filter_set()
            context['tasks'] = self.get_filter_set().qs
        return context


def add_note(request, group_id):
    """Add a note to a group."""
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        text = request.POST.get('note', '')
        Note.objects.create(group=group, note_text=text)
        messages.success(request, 'create note successful')
        return redirect(reverse('kuhub:group_detail', args=(group_id,)))


def delete_note(request, note_id):
    """Delete a note from a group."""
    note = get_object_or_404(Note, pk=note_id)
    group_id = note.group.id
    note.delete()
    messages.success(request, 'delete note successful')
    return redirect(reverse('kuhub:group_detail', args=(group_id,)))
