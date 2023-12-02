"""Module for display a list of all summary posts."""
from django.db.models import QuerySet
from django.views import generic
from kuhub.filters import PostDownloadFilter
from kuhub.models import PostDownload, Profile
from kuhub.views import FirebaseFolder, ProfileSetting


class SummaryHubView(generic.ListView):
    """Redirect to Summary-Hub page for summary posts."""

    queryset = ((PostDownload.objects
                .select_related('post_id__tag_id'))
                .order_by('-post_id__post_date').all())
    template_name: str = 'kuhub/summary.html'
    context_object_name: str = 'summary_post_list'

    def __init__(self):
        """Initialize SummaryHubView."""
        super().__init__()
        self.filterset = None

    def get_queryset(self) -> QuerySet[PostDownload]:
        """Return PostDownload objects with tag_id=2 and order by post_date."""
        queryset = super().get_queryset()
        self.filterset = PostDownloadFilter(
            self.request.GET,
            queryset=queryset
        )
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Get context data icon styles, profiles list and form."""
        context = super().get_context_data(**kwargs)

        profiles_list = [
            Profile.objects.filter(user=post.post_id.username).first()
            for post in context['summary_post_list']
        ]
        context['like_icon_styles'] = [
            post.like_icon_style(self.request.user)
            for post in context['summary_post_list']
        ]
        context['dislike_icon_styles'] = [
            post.dislike_icon_style(self.request.user)
            for post in context['summary_post_list']
        ]
        context['profiles_list'] = profiles_list
        context['form'] = self.filterset.form

        file_store_summary = (
            FirebaseFolder.separate_folder_firebase('summary-file/'))
        file_store_profile = (
            FirebaseFolder.separate_folder_firebase('profile/'))

        # Display Profile in Navbar
        ProfileSetting.update_display_photo(
            profile=self.request.user.profile,
            firebase_folder='profile/',
            user=self.request.user
        )

        # Change file name into url
        for post_sheet in context['summary_post_list']:
            post_sheet.post_id.username.profile.display_photo = (
                file_store_profile)[
                post_sheet.post_id.username.profile.display_photo]
            post_sheet.file = file_store_summary[post_sheet.file.name]

        return context
