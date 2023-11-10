"""Import Post and PostDownload models"""
from django.views import generic
from kuhub.models import Post, PostDownload
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

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


@login_required
def like_post(request: HttpRequest):
    if request.method == 'POST':
        post_id = request.POST.get('post_id', 0)
        post_obj = get_object_or_404(Post, id=post_id)
        user = request.user

        if user in post_obj.disliked.all():
            post_obj.disliked.remove(user)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

    return redirect('kuhub:review')


@login_required
def dislike_post(request: HttpRequest):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = get_object_or_404(Post, id=post_id)
        user = request.user

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)

        if user in post_obj.disliked.all():
            post_obj.disliked.remove(user)
        else:
            post_obj.disliked.add(user)

    return redirect('kuhub:review')
