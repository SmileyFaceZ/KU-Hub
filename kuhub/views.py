"""Contains view functions for handling requests.

related to Review-Hub, Summary-Hub and Tricks-Hub
in the kuhub web application.
"""
import datetime as dt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import generic
from kuhub.forms import PostForm
from kuhub.models import Post, PostDownload, Tags


class ReviewHubView(generic.ListView):
    """Redirect to Review-Hub page for review posts."""

    template_name: str = 'kuhub/review.html'
    context_object_name: str = 'posts_list'

    def get_queryset(self) -> QuerySet[Post]:
        """Return Post objects with tag_id=1 and order by post_date."""
        return Post.objects.filter(tag_id=1).order_by('-post_date')


class SummaryHubView(generic.ListView):
    """Redirect to Summary-Hub page for summary posts."""

    template_name: str = 'kuhub/summary.html'
    context_object_name: str = 'summary_post_list'

    def get_queryset(self) -> QuerySet[PostDownload]:
        """Return PostDownload objects with tag_id=2 and order by post_date."""
        return PostDownload.objects.select_related('post_id__tag_id').order_by(
            '-post_id__post_date'
        ).all()


class TricksHubView(generic.ListView):
    """Redirect to Tricks-Hub page for tricks posts."""

    template_name: str = 'kuhub/tricks.html'
    context_object_name: str = 'posts_list'

    def get_queryset(self) -> QuerySet[Post]:
        """Return Post objects with tag_id=3 and order by post_date."""
        return Post.objects.filter(tag_id=3).order_by('-post_date')


class EncouragementView(generic.ListView):
    """Redirect to Encouragement page for encouragement posts."""

    template_name: str = 'kuhub/encourage.html'
    context_object_name: str = 'posts_list'

    def get_queryset(self) -> QuerySet[Post]:
        """Return Post objects with tag_id=4 and order by post_date."""
        return Post.objects.filter(tag_id=4).order_by('-post_date')


@login_required
def create_post(request: HttpRequest):
    """Create post of each tag type and redirect to each tag page."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            post = Post.objects.create(
                username=request.user,
                post_content=data['review'],
                post_date=dt.datetime.now(),
                post_likes=0,
                post_dislikes=0,
                tag_id=Tags.objects.get(tag_text=data['tag_name'])
            )

            messages.success(request, 'Create Post Successfully!')

            if data['tag_name'] == 'Review-Hub':
                return redirect('kuhub:review')

            if data['tag_name'] == 'Summary-Hub':
                PostDownload.objects.create(
                    post_id=post,
                    file=request.FILES.get('file_upload'),
                    download_date=dt.datetime.now(),
                    download_count=0,
                )
                return redirect('kuhub:summary')

            if data['tag_name'] == 'Tricks-Hub':
                return redirect('kuhub:tricks')

            if data['tag_name'] == 'Encouragement':
                return redirect('kuhub:encourage')

        return render(
            request,
            template_name='kuhub/form.html',
            context={'form': form}
        )

    return render(
        request,
        template_name='kuhub/form.html',
        context={
            "tags_list": Tags.objects.all(),
            "form": PostForm(),
        }
    )
