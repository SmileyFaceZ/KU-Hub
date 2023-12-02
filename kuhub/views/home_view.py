from django.contrib import messages
from django.views import generic
from kuhub.models import Post, Profile, UserFollower
from kuhub.filters import PostFilter
from kuhub.views.profile.profile_setting import ProfileSetting
from kuhub.views.firebase_folder import FirebaseFolder


class HomePageView(generic.ListView):
    template_name = 'kuhub/home_page.html'
    context_object_name: str = 'followed_users_posts'

    def get_queryset(self):
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

        # Display Profile in Navbar
        ProfileSetting.update_display_photo(
            profile=self.request.user.profile,
            firebase_folder='profile/',
            user=self.request.user
        )
        file_store_profile = FirebaseFolder.separate_folder_firebase(
            'profile/')

        for post in context[self.context_object_name]:
            post.username.profile.display_photo = file_store_profile[post.username.profile.display_photo]

        # Check if the user is authenticated
        if self.request.user.is_authenticated:
            followed_users = UserFollower.objects.filter(follower=self.request.user).values_list('user_followed', flat=True)
            followed_users_posts = Post.objects.filter(username__in=followed_users).order_by('-post_date')

            # Check if the user is following anyone
            if not followed_users.exists():
                messages.info(self.request, "You are not following anyone yet.")

            queryset = followed_users_posts
            self.filterset = PostFilter(self.request.GET, queryset=queryset)
            context['followed_users_posts'] = self.filterset.qs
            context['like_icon_styles'] = [post.like_icon_style(self.request.user) for post in context['followed_users_posts']]
            context['dislike_icon_styles'] = [post.dislike_icon_style(self.request.user) for post in context['followed_users_posts']]

        else:
            # User is not authenticated, display a message
            messages.info(self.request, "Please log in to see posts from people you follow.")

            # Provide an empty queryset to prevent errors
            context['followed_users_posts'] = Post.objects.none()

        # Include search form in the context
        context['form'] = getattr(self, 'filterset', None) and getattr(self.filterset, 'form', None)

        # Include profiles list in the context
        context['profiles_list'] = [Profile.objects.filter(user=post.username).first() for post in context['followed_users_posts']]

        # Display profile photo in each post
        for post in context['followed_users_posts']:
            post.username.profile.display_photo = FirebaseFolder.separate_folder_firebase('profile/')[post.username.profile.display_photo]

        return context
