"""Module represent a list of all group from group database."""
from django.views import generic
from kuhub.models import Group
from kuhub.views.profile.profile_setting import ProfileSetting


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

        # Display Profile in Navbar
        ProfileSetting.update_display_photo(
            profile=self.request.user.profile,
            firebase_folder='profile/',
            user=self.request.user
        )
        return context
