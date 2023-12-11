"""This module define views for Review and Tricks Hub pages in application."""
from django.db.models import QuerySet
from django.views import generic
from kuhub.filters import PostFilter
from kuhub.models import Post, Profile
from kuhub.views.firebase_folder import FirebaseFolder
from kuhub.views import ProfileSetting


class BaseHubView(generic.ListView):
    """Base class for Hub views."""

    tag_id = None
    template_name = None
    context_object_name = None

    def __init__(self):
        """Initialize BaseHubView."""
        super().__init__()
        self.filterset = None
        self.queryset = (Post.objects.all()
                         .filter(tag_id=self.tag_id)
                         .order_by('-post_date'))

    def get_queryset(self) -> QuerySet[Post]:
        """Return Post objects with tag_id and order by post_date."""
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Get context data icon styles, profiles list, and form."""
        context = super().get_context_data(**kwargs)

        profiles_list = [Profile.objects.filter(user=post.username).first()
                         for post in context[self.context_object_name]]

        context['like_icon_styles'] = [
            post.like_icon_style(self.request.user)
            for post in context[self.context_object_name]]
        context['dislike_icon_styles'] = [
            post.dislike_icon_style(self.request.user)
            for post in context[self.context_object_name]]
        context['profiles_list'] = profiles_list
        context['form'] = self.filterset.form

        file_store_profile = FirebaseFolder.separate_folder_firebase(
            'profile/')

        if self.request.user.is_authenticated:
            ProfileSetting.update_display_photo(
                profile=self.request.user.profile,
                firebase_folder='profile/',
                user=self.request.user
            )

            for post in context[self.context_object_name]:
                post.username.profile.display_photo = file_store_profile.get(
                    post.username.profile.display_photo, 'default_image.jpg')

        else:
            for post in context[self.context_object_name]:
                post.username.profile.display_photo = file_store_profile[
                    post.username.profile.display_photo]

        return context


class ReviewHubView(BaseHubView):
    """Redirect to Review-Hub page for review posts."""

    tag_id: int = 1
    template_name: str = 'kuhub/review.html'
    context_object_name: str = 'posts_list'


class TricksHubView(BaseHubView):
    """Redirect to Tricks-Hub page for tricks posts."""

    tag_id: int = 3
    template_name: str = 'kuhub/tricks.html'
    context_object_name: str = 'tricks_list'
