from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from kuhub.models import Group, GroupTags, GroupPassword
from kuhub.forms import GroupForm
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
import logging

LOGGER = logging.getLogger("kuhub")


def is_user_a_member(request: HttpRequest, group: Group):
    user = request.user
    if group.group_member.filter(pk=user.pk).exists():
        messages.warning(request, "You are already a member of this group.")
        return True
    return False


def is_password_protected(request: HttpRequest, group: Group):
    if group.group_password and request.method == 'POST':
        password = request.POST.get('pass')
        if password and not group.group_password.check_password(password):
            messages.error(request, "Wrong password.")
            return True
    return False


class GroupFeature:

    @staticmethod
    def is_user_a_member(self, group: Group, user: User):
        if group.group_member.filter(pk=user.pk).exists():
            messages.error(self.request, "You are already a member of this group.")
            return True
        return False

    @staticmethod
    # @method_decorator(login_required(login_url='/accounts/login/'))
    def join(request: HttpRequest, group_id: int):
        user = request.user
        group = get_object_or_404(Group, pk=group_id)

        if is_user_a_member(request, group):
            return redirect(reverse('kuhub:groups'))

        if is_password_protected(request, group):
            return redirect(reverse('kuhub:groups'))

        group.group_member.add(user)
        messages.success(request, "You have successfully joined the group!")
        return redirect(reverse('kuhub:groups'))

    @method_decorator(login_required)
    def create_group(self):
        if self.request.method == 'POST':
            form = GroupForm(self.request.POST)
            if form.is_valid():
                return self._process_group_form(form)
            else:
                messages.error(self.request, "Form data is not valid.")

        return render(
            self.request,
            'kuhub/group_create.html',
            {'form': GroupForm()}
        )

    def _process_group_form(self, form):
        data = form.cleaned_data
        if data['password'] != data['password_2']:
            messages.error(self.request, "Passwords do not match.")
            return render(
                self.request,
                'kuhub/group_create.html',
                {'form': form}
            )
        # if not have the tag in groupTag object create it
        group_tag, _ = GroupTags.objects.get_or_create(
            tag_text=data['tag_name'])

        # create group object
        password = None
        if data['password']:
            password = GroupPassword.objects.create(
                group_password=data['password'])
            password.set_password(data['password'])

        group = Group.objects.create(
            group_name=data['name'],
            group_description=data['description'],
            group_password=password,
        )
        group.group_tags.set([group_tag])
        group.group_member.add(self.request.user)

        messages.success(self.request, f'Group created successfully. Your group ID is {group.id}.')
        return redirect(reverse('kuhub:groups'))
