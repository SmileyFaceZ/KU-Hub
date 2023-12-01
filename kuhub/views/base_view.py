from django.db.models import QuerySet
from django.views import generic
from kuhub.filters import PostFilter, PostDownloadFilter
from kuhub.models import Post, Profile, PostDownload, UserFollower
from django.contrib import messages
from kuhub.views.firebase_view import navbar_setting_profile, separate_folder_firebase


class HomePageView(generic.ListView):
    template_name = 'kuhub/home_page.html'
    context_object_name: str = 'followed_users_posts'

    def get_queryset(self):
        navbar_setting_profile(self.request)
        if not self.request.user.is_authenticated:
            messages.info(self.request, "Please login first")
            return Post.objects.none()

        followed_users = UserFollower.objects.filter(follower=self.request.user).values_list('user_followed', flat=True)
        followed_users_posts = Post.objects.filter(username__in=followed_users).order_by('-post_date')

        if not followed_users.exists():
            return followed_users_posts.none()

        self.filterset = PostFilter(self.request.GET, queryset=followed_users_posts)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Add like and dislike icon styles and search form to context."""
        context = super().get_context_data(**kwargs)

        # Check if the user is authenticated
        if self.request.user.is_authenticated:
            followed_users = UserFollower.objects.filter(follower=self.request.user).values_list('user_followed',
                                                                                                 flat=True)
            followed_users_posts = Post.objects.filter(username__in=followed_users).order_by('-post_date')

            # Check if the user is following anyone
            if not followed_users.exists():
                messages.info(self.request, "You are not following anyone yet.")

            queryset = followed_users_posts
            self.filterset = PostFilter(self.request.GET, queryset=queryset)
            context['followed_users_posts'] = self.filterset.qs
            context['like_icon_styles'] = [post.like_icon_style(self.request.user) for post in
                                           context['followed_users_posts']]
            context['dislike_icon_styles'] = [post.dislike_icon_style(self.request.user) for post in
                                              context['followed_users_posts']]

        else:
            # User is not authenticated, display a message
            messages.info(self.request, "Please log in to see posts from people you follow.")

            # Provide an empty queryset to prevent errors
            context['followed_users_posts'] = Post.objects.none()

        # Include search form in the context
        context['form'] = getattr(self, 'filterset', None) and getattr(self.filterset, 'form', None)

        # Include profiles list in the context
        context['profiles_list'] = [Profile.objects.filter(user=post.username).first() for post in
                                    context['followed_users_posts']]

        # Display profile photo in each post
        for post in context['followed_users_posts']:
            post.username.profile.display_photo = separate_folder_firebase('profile/')[
                post.username.profile.display_photo]

        return context


class ReviewHubView(generic.ListView):
    """Redirect to Review-Hub page for review posts."""
    queryset = Post.objects.all().filter(tag_id=1).order_by('-post_date')
    template_name: str = 'kuhub/review.html'
    context_object_name: str = 'posts_list'

    def get_queryset(self) -> QuerySet[Post]:
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Add like and dislike icon styles to context."""
        context = super().get_context_data(**kwargs)

        profiles_list = [Profile.objects.filter(user=post.username).first()
                         for post in context['posts_list']]

        context['like_icon_styles'] = [post.like_icon_style(self.request.user)
                                       for post in context['posts_list']]
        context['dislike_icon_styles'] = [
            post.dislike_icon_style(self.request.user) for post in
            context['posts_list']]
        context['profiles_list'] = profiles_list

        context['form'] = self.filterset.form

        navbar_setting_profile(self.request)

        for post in context['posts_list']:
            try:
                post.username.profile.display_photo = separate_folder_firebase('profile/')[
                    post.username.profile.display_photo]
            except TypeError:
                post.username.profile.display_photo = {}
        return context


class SummaryHubView(generic.ListView):
    """Redirect to Summary-Hub page for summary posts."""

    queryset = ((PostDownload.objects
                 .select_related('post_id__tag_id'))
                .order_by('-post_id__post_date').all())
    template_name: str = 'kuhub/summary.html'
    context_object_name: str = 'summary_post_list'

    def get_queryset(self) -> QuerySet[PostDownload]:
        """Return PostDownload objects with tag_id=2 and order by post_date."""
        queryset = super().get_queryset()
        self.filterset = PostDownloadFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Add like and dislike icon styles to context."""
        context = super().get_context_data(**kwargs)

        file_store_summary = separate_folder_firebase('summary-file/')
        file_store_profile = separate_folder_firebase('profile/')

        # Contain Profile Name
        context['like_icon_styles'] = [post.like_icon_style(self.request.user)
                                       for post in context['summary_post_list']]
        context['dislike_icon_styles'] = [
            post.dislike_icon_style(self.request.user) for post in
            context['summary_post_list']
        ]

        context['form'] = self.filterset.form

        # Change file name into url
        for i in context['summary_post_list']:
            i.post_id.username.profile.display_photo = file_store_profile[i.post_id.username.profile.display_photo]
            i.file = file_store_summary[i.file.name]

        navbar_setting_profile(self.request)

        return context


class TricksHubView(generic.ListView):
    """Redirect to Tricks-Hub page for tricks posts."""

    queryset = Post.objects.filter(tag_id=3).order_by('-post_date')
    template_name: str = 'kuhub/tricks.html'
    context_object_name: str = 'tricks_list'

    def get_queryset(self) -> QuerySet[Post]:
        """Return Post objects with tag_id=3 and order by post_date."""
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Add like and dislike icon styles to context."""
        context = super().get_context_data(**kwargs)

        profiles_list = [Profile.objects.filter(user=post.username).first()
                         for post in context['tricks_list']]

        context['like_icon_styles'] = [post.like_icon_style(self.request.user)
                                       for post in context['tricks_list']]
        context['dislike_icon_styles'] = [
            post.dislike_icon_style(self.request.user) for post in
            context['tricks_list']]
        context['profiles_list'] = profiles_list
        context['form'] = self.filterset.form

        for post in context['tricks_list']:
            post.username.profile.display_photo = separate_folder_firebase('profile/')[
                post.username.profile.display_photo]

        navbar_setting_profile(self.request)

        return context