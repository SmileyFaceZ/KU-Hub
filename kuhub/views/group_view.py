"""Module represent a list of all group from group database."""
from django.views import generic
from kuhub.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from kuhub.forms import GroupForm
from kuhub.models import GroupTags, GroupPassword
from django.urls import reverse
from django.http import HttpRequest


class GroupView(generic.ListView):
    """Redirect to Group-Hub page."""

    template_name = 'kuhub/group.html'
    context_object_name = 'group_list'

    def get_queryset(self):
        """Return most 100 recent group posts."""
        return Group.objects.all().order_by('-create_date')[:100]

    def get_context_data(self, **kwargs):
        """Return user'group data as contect data."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_groups'] = self.request.user.group_set.all()
        return context


@login_required
def join(request, group_id):
    """Register user to group and display a group that user join."""
    user = request.user
    group = get_object_or_404(Group, pk=group_id)
    if user in group.group_member.all():
        messages.error(request, "You already a member of this group")
        return redirect(reverse('kuhub:groups'))
    if group.group_password:
        if request.method == 'POST':
            password = request.POST['pass']
            if not group.group_password.check_password(password):
                messages.error(request, "Wrong password")
                return redirect(reverse('kuhub:groups'))
    group.group_member.add(user)
    messages.success(request, "You join the group success!")
    return redirect(reverse('kuhub:groups'))


@login_required
def create_group(request: HttpRequest):
    """Create Group when user click create group button."""
    user = request.user
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # check password and password(again) is the same
            if data['password'] != data['password_2']:
                messages.error(request, "Password is not the same")
                return render(
                    request,
                    template_name='kuhub/group_create.html',
                    context={'form': GroupForm}
                )
            # if not have the tag in groupTag object create it
            group_tag, created = (
                GroupTags.objects.get_or_create(tag_text=data['tag_name'])
            )
            # create group object
            password = None
            if data['password']:
                password = (
                    GroupPassword.objects.create(
                        group_password=data['password']
                    )
                )
                password.set_password(password.group_password)
            group = Group.objects.create(
                group_name=data['name'],
                group_description=data['description'],
                group_password=password,
            )
            group.group_tags.set([group_tag])
            group.group_member.set([user])
            messages.success(
                request,
                f'Create group successful your group id is {group.id}'
            )
            return redirect(reverse('kuhub:groups'))
    return render(
        request,
        template_name='kuhub/group_create.html',
        context={'form': GroupForm}
    )
