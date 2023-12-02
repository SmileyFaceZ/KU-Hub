"""Module for managing group features in application."""
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from kuhub.models import Group, GroupTags, GroupPassword
from kuhub.forms import GroupForm
from django.contrib.auth.models import User
from kuhub.views.profile.profile_setting import ProfileSetting


class GroupFeature:
    """A class for handling various group-related features."""

    @staticmethod
    def is_password_protected(request: HttpRequest, group: Group) -> bool:
        """Check if the user is already a member of the specified group.

        :param request: The HTTP request object.
        :param group: The group to check membership for.
        :return: True if the user is a member, False otherwise.
        """
        if group.group_password and request.method == 'POST':
            password = request.POST.get('pass')
            if password and not group.group_password.check_password(password):
                messages.error(request, "Wrong password.")
                return True
        return False

    @staticmethod
    def is_user_a_member(request: HttpRequest, group: Group,
                         user: User) -> bool:
        """Check if the provided password is correct.

        :param request: The HTTP request object.
        :param group: The group to check for password protection.
        :return: True if password protected and password is incorrect,
        False otherwise.
        """
        if group.group_member.filter(pk=user.pk).exists():
            messages.error(
                request,
                "You are already a member of this group.")
            return True
        return False

    @staticmethod
    def join(request: HttpRequest, group_id: int):
        """Handle the process of a user joining a group.

        :param request: The HTTP request object.
        :param group_id: The ID of the group to join.
        :return: Redirects to the groups page.
        """
        user = request.user
        group = get_object_or_404(Group, pk=group_id)

        if GroupFeature.is_user_a_member(request, group):
            return redirect(reverse('kuhub:groups'))

        if GroupFeature.is_password_protected(request, group):
            return redirect(reverse('kuhub:groups'))

        group.group_member.add(user)
        messages.success(
            request,
            "You have successfully joined the group!")
        return redirect(reverse('kuhub:groups'))

    @staticmethod
    def process_group_form(request: HttpRequest, form: GroupForm):
        """Process the group creation form and create a new group if valid.

        :param request: The HTTP request object.
        :param form: The form containing group data.
        :return: Redirects to the groups page or re-renders the form on error.
        """
        data = form.cleaned_data
        if data['password'] != data['password_2']:
            messages.error(request, "Passwords do not match.")
            return render(
                request,
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
        group.group_member.add(request.user)

        messages.success(
            request,
            f'Group created successfully. Your group ID is {group.id}.')
        return redirect(reverse('kuhub:groups'))

    @staticmethod
    def create_group(request: HttpRequest):
        """Display the group creation form and process it upon submission.

        :param request: The HTTP request object.
        :return: Renders the group creation form or redirects after processing.
        """
        # Display Profile in Navbar
        ProfileSetting.update_display_photo(
            profile=request.user.profile,
            firebase_folder='profile/',
            user=request.user
        )
        if request.method == 'POST':
            form = GroupForm(request.POST)
            if form.is_valid():
                return GroupFeature.process_group_form(request, form)
            else:
                messages.error(request, "Form data is not valid.")

        return render(
            request,
            'kuhub/group_create.html',
            {'form': GroupForm()}
        )
