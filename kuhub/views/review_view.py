"""Module for display a list of all review posts."""
from django.db.models import QuerySet
from django.views import generic
from kuhub.filters import PostFilter
from kuhub.models import Post, Profile


class ReviewHubView(generic.ListView):
    """Redirect to Review-Hub page for review posts."""

    queryset = Post.objects.all().filter(tag_id=1).order_by('-post_date')
    template_name: str = 'kuhub/review.html'
    context_object_name: str = 'posts_list'

    def __init__(self):
        """Initialize ReviewHubView."""
        super().__init__()
        self.filterset = None

    def get_queryset(self) -> QuerySet[Post]:
        """Return review post that filter by user input."""
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Get context data icon styles, profiles list and form."""
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

        return context
