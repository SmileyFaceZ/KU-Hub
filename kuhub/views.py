"""Import Post and PostDownload models"""
from django.views import generic
from kuhub.models import Post, PostDownload

# Create your views here.


class ReviewHubView(generic.ListView):
    """
    Redirect to Review-Hub page.
    """
    template_name = 'kuhub/review.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        """Return recently published review posts."""
        return Post.objects.filter(tag_id=1).order_by('-post_date')


class SummaryHubView(generic.ListView):
    """
    Redirect to Summary-Hub page.
    """
    template_name = 'kuhub/summary.html'
    context_object_name = 'summary_post_list'

    def get_queryset(self):
        """Return summary posts queryset."""
        return PostDownload.objects.select_related('post_id__tag_id').all()


class TricksHubView(generic.ListView):
    """
    Redirect to Tricks-Hub page.
    """
    template_name = 'kuhub/tricks.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        """Return recently published trick posts."""
        return Post.objects.filter(tag_id=3).order_by('-post_date')


class EncouragementView(generic.ListView):
    """
    Redirect to Encouragement page.
    """
    template_name = 'kuhub/encourage.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        """Return recently published encourage posts."""
        return Post.objects.filter(tag_id=4).order_by('-post_date')
