"""Module to represent a list of all subject type from database."""
from django.views import generic
from kuhub.models import Subject
from kuhub.filters import GenedFilter
from kuhub.views.profile.profile_setting import ProfileSetting


class GenEdTypeListView(generic.ListView):
    """Redirect to show a type all subject type list."""

    template_name = 'kuhub/gened_list.html'
    context_object_name = 'type_list'

    def get_queryset(self):
        """Return QuerySet of all subjects ordered by course_code."""
        tag_list = (Subject.objects.values_list("type", flat=True)
                    .distinct().order_by('type'))
        return [tag.replace("_", " ") for tag in tag_list]

    def get_context_data(self, **kwargs):
        """Return user'group data as contect data."""
        context = super().get_context_data(**kwargs)
        subject_list = Subject.objects.all().order_by('course_code')

        subject_filter = GenedFilter(
            self.request.GET,
            queryset=subject_list
        )
        for subject in subject_filter.qs:
            subject.type = subject.type.replace("_", " ")

        context['subject_list'] = subject_filter.qs
        context['form'] = subject_filter.form

        # Display Profile in Navbar only if user is authenticated
        if self.request.user.is_authenticated:
            ProfileSetting.update_display_photo(
                profile=self.request.user.profile,
                firebase_folder='profile/',
                user=self.request.user
            )

        return context
