from kuhub.models import Group, GroupEvent, Task
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404, render


def add_task(request, group_id):
    user = request.user
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        text = request.POST.get('task', '')
        status = request.POST.get('status', '')
        event_get = request.POST.get('assign_to_event', '')
        print(event_get)
        if event_get == 'not assign':
            event = None
        else:
            event = get_object_or_404(GroupEvent, pk=event_get)
        Task.objects.create(group=group, task_text=text, status=status, assign_user=user, event=event)
        messages.success(request, 'create task successful')
        previous_path = request.META.get('HTTP_REFERER', None)
        if 'event' in str(previous_path):
            return redirect(reverse('kuhub:event_detail', args=(event.id,)))
        return redirect(reverse('kuhub:group_detail', args=(group_id,)))

def change_task_status(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    group_id = task.group.id
    if request.method == 'POST':
        status = request.POST.get('status', '')
        task.status = status
        task.save()
        messages.success(request, 'Change status successful')
    previous_path = request.META.get('HTTP_REFERER', None)
    if 'event' in str(previous_path):
        return redirect(reverse('kuhub:event_detail', args=(task.event.id,)))
    return redirect(reverse('kuhub:group_detail', args=(group_id,)))

def delete_task(request, note_id):
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

def assign_task_in_event(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    group_id = task.group.id
    if request.method == 'POST':
        event_id = request.POST.get('assign_to_event', '')
        print(event_id)
        event = get_object_or_404(GroupEvent, pk=event_id)
        task.event = event
        task.save()
        messages.success(request, 'assign to event successfully!')
    return redirect(reverse('kuhub:group_detail', args=(group_id,)))

def unassign_task(request, task_id):
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
