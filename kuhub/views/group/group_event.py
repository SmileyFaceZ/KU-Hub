"""Controller for managing group events, tasks, and notes in application."""
import logging
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from kuhub.forms import EventForm
from kuhub.models import Group, GroupEvent, Note, Task
from kuhub.calendar import create_event
from django.http import HttpRequest, Http404


class GroupEventController:
    """Creating and managing group events, adding, deleting notes and tasks."""

    @staticmethod
    def group_event_create(request: HttpRequest, group_id: int):
        """To creates a group event based on user input.

        :param request: HttpRequest object.
        :param group_id: Integer representing the group's ID.
        :return: Redirects to the group event creation page
        or the group detail page.
        """
        user = request.user
        is_google_user = user.socialaccount_set.filter(
            provider='google').exists()
        try:
            group = get_object_or_404(Group, pk=group_id)
        except Http404:
            messages.warning('Not have this group id!.')
            return redirect('kuhub:groups')

        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                return GroupEventController.handle_valid_form(
                    request=request,
                    form=form,
                    group=group,
                    group_id=group_id)

        return render(
            request,
            'kuhub/group_event.html',
            {
                'form': EventForm(),
                'group': group,
                'user': user,
                'is_google': is_google_user
            }
        )

    @staticmethod
    def handle_valid_form(request: HttpRequest, form: EventForm, group: Group,
                          group_id: int):
        """To handles a valid form submission for a group event.

        :param request: HttpRequest object.
        :param form: EventForm instance with submitted data.
        :param group: Group instance where the event is being created.
        :param group_id: Integer representing the group's ID.
        :return: Redirects to the group detail page.
        """
        data = form.cleaned_data
        group_event = GroupEvent.objects.create(
            group=group,
            summary=data['summary'],
            location=data['location'],
            description=data['description'],
            start_time=data['start_time'].strftime('%Y-%m-%dT%H:%M:%S'),
            end_time=data['end_time'].strftime('%Y-%m-%dT%H:%M:%S'),
            show_time=f"{data['start_time'].strftime('%a. %d %b %Y %H:%M:%S')}"
                      f" - "
                      f"{data['end_time'].strftime('%a. %d %b %Y %H:%M:%S')}"
        )

        if data['is_meeting']:
            meet_link = GroupEventController.has_meeting(request, group_id,
                                                         data)
            if meet_link:
                group_event.link = meet_link
                group_event.save()
                messages.success(
                    request,
                    'Event created successfully')
                return redirect(
                    reverse('kuhub:group_detail', args=(group_id,)))

        messages.success(request, 'Event created successfully')
        return redirect(reverse(
            'kuhub:group_detail',
            args=(group_id,)))

    @staticmethod
    def has_meeting(request: HttpRequest, group_id: int, data: dict) -> str:
        """To creates a meeting link for a group event.

        :param request: HttpRequest object.
        :param group_id: Integer representing the group's ID.
        :param data: Dictionary containing event details.
        :return: String URL of the meeting link.
        """
        try:
            event, meet_link = create_event(
                request=request,
                summary=data['summary'],
                description=data['description'],
                location=data['location'],
                start_datetime=data['start_time'].strftime(
                    '%Y-%m-%dT%H:%M:%S'),
                end_datetime=data['end_time'].strftime('%Y-%m-%dT%H:%M:%S')
            )
            return meet_link
        except Exception as error_message:
            messages.error(
                request,
                "You have to login with Google before "
                "using this feature")
            logging.getLogger('kuhub').error(
                f"Error when creating meeting for group "
                f"{group_id}: {error_message}")
            return ''

    @staticmethod
    def add_note(request: HttpRequest, group_id: int):
        """To adds a note to a specified group.

        :param request: The HttpRequest object.
        :param group_id: The ID of the group to which the note will be added.
        :return: A redirect to the group detail page or groups list.
        """
        try:
            group = get_object_or_404(Group, pk=group_id)
        except Http404:
            messages.warning('Not have this group id!.')
            return redirect('kuhub:groups')

        if request.method == 'POST':
            text = request.POST.get('note', '')
            Note.objects.create(group=group, note_text=text)
            messages.success(request, 'Note added successfully')
            return redirect(reverse(
                'kuhub:group_detail',
                args=(group_id,)))

    @staticmethod
    def delete_note(request: HttpRequest, note_id: int):
        """To deletes a note based on the provided note ID.

        :param request: The HttpRequest object.
        :param note_id: The ID of the note to be deleted.
        :return: A redirect to the group detail page.
        """
        note = get_object_or_404(Note, pk=note_id)
        group_id = note.group.id
        note.delete()
        messages.success(request, 'Note deleted successfully')
        return redirect(reverse(
            'kuhub:group_detail',
            args=(group_id,)))

    @staticmethod
    def add_task(request: HttpRequest, group_id: int):
        """To adds a task to a specified group.

        :param request: The HttpRequest object.
        :param group_id: The ID of the group to which the task will be added.
        :return: A redirect to the group detail or event detail page.
        """
        user = request.user
        try:
            group = get_object_or_404(Group, pk=group_id)
        except Http404:
            messages.warning(request, "Not have this group id!.")
            redirect('kuhub:groups')

        if request.method == 'POST':
            text = request.POST.get('task', '')
            status = request.POST.get('status', '')
            event_get = request.POST.get('assign_to_event', '')

            event = None
            if event_get != 'not assign':
                event = get_object_or_404(GroupEvent, pk=event_get)

            Task.objects.create(group=group, task_text=text, status=status,
                                assign_user=user, event=event)
            messages.success(request, 'create task successful')
            previous_path = request.META.get('HTTP_REFERER', None)
            if 'event' in str(previous_path):
                return redirect(
                    reverse('kuhub:event_detail', args=(event.id,)))
            return redirect(reverse('kuhub:group_detail', args=(group_id,)))

    @staticmethod
    def delete_task(request: HttpRequest, note_id: int):
        """To deletes a task based on the provided task ID.

        :param request: The HttpRequest object.
        :param note_id: The ID of the task to be deleted.
        :return: A redirect to either the group detail or event detail page.
        """
        task = get_object_or_404(Task, pk=note_id)
        group_id = task.group.id
        event_id = None
        if task.event:
            event_id = task.event.id
        task.delete()
        messages.success(request, 'delete task successful')
        previous_path = request.META.get('HTTP_REFERER', None)
        if 'event' in str(previous_path):
            return redirect(reverse('kuhub:event_detail', args=(event_id,)))
        return redirect(reverse('kuhub:group_detail', args=(group_id,)))

    @staticmethod
    def change_task_status(request: HttpRequest, task_id: int):
        """To changes the status of a task and redirects to the appropriate page.

        :param request: The HttpRequest object.
        :param task_id: The ID of the task whose status will be changed.
        :return: A redirect to either the group detail or event detail page.
        """
        task = get_object_or_404(Task, pk=task_id)
        group_id = task.group.id
        if request.method == 'POST':
            status = request.POST.get('status', '')
            task.status = status
            task.save()
            messages.success(request, 'Change status successful')
        previous_path = request.META.get('HTTP_REFERER', None)
        if 'event' in str(previous_path):
            return redirect(
                reverse('kuhub:event_detail', args=(task.event.id,)))
        return redirect(reverse('kuhub:group_detail', args=(group_id,)))

    @staticmethod
    def assign_task_in_event(request: HttpRequest, task_id: int):
        """To assigns a task to an event and redirects to the group detail page.

        :param request: The HttpRequest object.
        :param task_id: The ID of the task to be assigned to an event.
        :return: A redirect to the group detail page.
        """
        task = get_object_or_404(Task, pk=task_id)
        group_id = task.group.id
        if request.method == 'POST':
            event_id = request.POST.get('assign_to_event', '')
            event = get_object_or_404(GroupEvent, pk=event_id)
            task.event = event
            task.save()
            messages.success(request, 'assign to event successfully!')
        return redirect(reverse('kuhub:group_detail', args=(group_id,)))

    @staticmethod
    def group_event_delete(request: HttpRequest, event_id: int):
        """To deletes a group event based on the provided event ID.

        :param request: The HttpRequest object.
        :param event_id: The ID of the event to be deleted.
        :return: A redirect to the group detail page.
        """
        event = get_object_or_404(GroupEvent, pk=event_id)
        group_id = event.group.id
        # delete GroupEvent object
        event.delete()
        messages.success(request, 'delete event successful')
        return redirect(reverse('kuhub:group_detail', args=(group_id,)))

    @staticmethod
    def unassign_task(request: HttpRequest, task_id: int):
        """Unassigns a task from an event.

        :param request: The HttpRequest object.
        :param task_id: The ID of the task to be unassigned.
        :return: A redirect to either the group detail or event detail page.
        """
        task = get_object_or_404(Task, pk=task_id)
        group_id = task.group.id
        event_id = task.event.id
        task.event = None
        task.save()
        messages.success(request, 'assign to event successfully!')
        previous_path = request.META.get('HTTP_REFERER', None)
        if 'event' in str(previous_path):
            return redirect(reverse('kuhub:event_detail', args=(event_id,)))
        return redirect(reverse('kuhub:group_detail', args=(group_id,)))
