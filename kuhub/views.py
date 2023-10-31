from kuhub.models import Post
from django.views import generic

# Create your views here.


class ReviewHubView(generic.ListView):
    template_name = 'kuhub/review.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        """Return recently published review posts."""
        return Post.objects.filter(tag_id=1).order_by('-post_date')


class SummaryHubView(generic.ListView):
    template_name = 'kuhub/summary.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        """Return recently published summary posts."""
        return Post.objects.order_by('-post_date')


class TricksHubView(generic.ListView):
    template_name = 'kuhub/tricks.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        """Return recently published trick posts."""
        return Post.objects.filter(tag_id=3).order_by('-post_date')


class EncouragementView(generic.ListView):
    template_name = 'kuhub/encourage.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        """Return recently published encourage posts."""
        return Post.objects.order_by('-post_date')
