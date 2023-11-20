from django.db.models.query import QuerySet
from django.views import generic
from kuhub.filters import PostFilter
from kuhub.models import Post, Profile


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

        return context
