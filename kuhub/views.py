"""Import Post and PostDownload models"""
from django.views import generic
from kuhub.models import Post, PostDownload, Tags
from kuhub.form import PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
import datetime as dt
from django.contrib import messages


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
        return PostDownload.objects.select_related('post_id__tag_id').order_by(
            '-post_id__post_date'
        ).all()


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
def create_post(request):
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

    context = {
        "tags_list": Tags.objects.all(),
        "form": PostForm(),
    }
    return render(
        request,
        template_name='kuhub/form.html',
        context=context
    )

