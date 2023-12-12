"""This module for manage and displaying detail information group."""
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from kuhub.models import Group
from kuhub.filters import TaskFilter
from django.shortcuts import redirect
from kuhub.views.profile.profile_setting import ProfileSetting
from typing import Any, Dict
from django.db.models.query import QuerySet
import logging


@method_decorator(login_required, name='dispatch')
class GroupDetail(generic.DetailView):
    """Group manage and detail page."""

    model = Group
    template_name = 'kuhub/group_detail.html'

    def get_queryset(self) -> QuerySet[Group]:
        """Return Query set ob Group model."""
        return Group.objects.all()

    def get_object(self, queryset: QuerySet[Group] = None) -> Group:
        """Retrieve group object, ensure the user is a member of the group."""
        obj = super().get_object(queryset)
        try:
            obj.group_member.filter(pk=self.request.user.pk).exists()
        except AttributeError as error_message:
            logging.getLogger("django.request").error(error_message)
            return redirect('kuhub:groups')

        return obj

    def get_filter_set(self) -> TaskFilter:
        """Generate a TaskFilter based on the current request."""
        return TaskFilter(
            self.request.GET,
            queryset=self.object.task_set.all()
        )

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """Return user'group data as contect data."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['events'] = self.object.groupevent_set.all()
            context['notes'] = self.object.note_set.all()
            context['filter'] = self.get_filter_set()
            context['tasks'] = self.get_filter_set().qs

        # Display Profile in Navbar
        ProfileSetting.update_display_photo(
            profile=self.request.user.profile,
            firebase_folder='profile/',
            user=self.request.user
        )
        return context
