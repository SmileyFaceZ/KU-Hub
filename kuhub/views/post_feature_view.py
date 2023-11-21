"""Module for feature that related to post."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from kuhub.forms import PostForm
from kuhub.models import Post, Tags, PostDownload, Subject, PostReport
from kuhub.forms import CommentForm
from kuhub.models import PostComments, Profile
from itertools import zip_longest
from django.db.models import Count
from kuhub.forms import ReportForm

import datetime as dt
import json


@login_required
def like_post(request: HttpRequest) -> JsonResponse:
    """Increase number of likes for a post when the user clicks the like."""
    user = request.user
    if user.is_authenticated:
        if (request.method == 'POST'
                and request.headers.get(
                    'X-Requested-With') == 'XMLHttpRequest'):
            post_id = request.readline().decode('utf-8')
            js_post = json.loads(post_id)
            post_obj = get_object_or_404(Post, id=js_post['post_id'])

            if user in post_obj.disliked.all():
                post_obj.disliked.remove(user)

            if user in post_obj.liked.all():
                post_obj.liked.remove(user)
            else:
                post_obj.liked.add(user)

            return JsonResponse(
                {
                    'likes': post_obj.liked.all().count(),
                    'dislikes': post_obj.disliked.all().count(),
                    'like_style': post_obj.like_icon_style(user),
                    'dislike_style': post_obj.dislike_icon_style(user)
                }
            )
        return redirect('kuhub:review')

    return redirect('account_login')


@login_required
def dislike_post(request: HttpRequest) -> JsonResponse:
    """Decrease number of likes for a post when the user clicks the dislike."""
    user = request.user
    if user.is_authenticated:
        if (request.method == 'POST'
                and request.headers.get(
                    'X-Requested-With') == 'XMLHttpRequest'):
            post_id = request.readline().decode('utf-8')
            js_post = json.loads(post_id)
            post_obj: Post = get_object_or_404(Post, id=js_post['post_id'])

            if user in post_obj.liked.all():
                post_obj.liked.remove(user)

            if user in post_obj.disliked.all():
                post_obj.disliked.remove(user)
            else:
                post_obj.disliked.add(user)

            return JsonResponse(
                {
                    'likes': post_obj.total_likes(),
                    'dislikes': post_obj.total_dislikes(),
                    'dislike_style': post_obj.dislike_icon_style(user),
                    'like_style': post_obj.like_icon_style(user),
                }
            )
        return redirect('kuhub:review')

    return redirect('account_login')


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


def post_detail(request, pk):
    """Display post detail and comment section."""
    post = get_object_or_404(Post, pk=pk)
    comments_list = PostComments.objects.filter(post_id=post)

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)

            if form.is_valid():
                data = form.cleaned_data['comment']
                PostComments.objects.create(username=request.user,
                                            post_id=post,
                                            comment=data,
                                            comment_date=dt.datetime.now())

        else:
            return redirect('account_login')
    else:
        form = CommentForm()

    owner_profile = Profile.objects.filter(user=post.username)
    comments_profiles = [Profile.objects.filter(user=comment.username).first()
                         for comment in comments_list]

    # Use zip_longest to handle different lengths
    comments_and_profiles = zip_longest(comments_list, comments_profiles)

    context = {
        'post': post,
        'comments_and_profiles': comments_and_profiles,
        'form': form,
        'owner_profile': owner_profile,
    }

    return render(request, 'kuhub/post_detail.html', context)


@login_required
def edit_post(request, pk):
    """User can edit their own post content, tag and subject."""
    try:
        post = get_object_or_404(Post, pk=pk)
    except Http404:
        messages.warning(
            request,
            f"Pos️t ID {pk} does not exist.❗️"
        )
        return redirect("kuhub:review")

    if request.user != post.username:
        messages.warning(
            request,
            "You are not the owner of this post.❗️"
        )

        return redirect(
            'kuhub:post_detail',
            pk=post.pk
        )

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            tag_name = form.cleaned_data['tag_name']

            tag = get_object_or_404(Tags, tag_text=tag_name)
            post.tag_id = tag

            subject_code = form.cleaned_data['subject']
            subject = get_object_or_404(Subject, course_code=subject_code)
            post.subject = subject

            post.post_content = form.cleaned_data['review']

            post.save()

            return redirect(
                'kuhub:post_detail',
                pk=post.pk
            )
    else:
        form = PostForm(
            initial={
                'tag_name': post.tag_id.tag_text,
                'subject': post.subject.course_code,
                'review': post.post_content
            }
        )

    return render(
        request,
        'kuhub/edit_post.html',
        {
            'form': form,
            'user': request.user,
            'post': post
        }
    )


def report_post(request, pk):
    """Report a post when user has a unacceptable content."""
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            report_count = (
                PostReport.objects.filter(
                    post_id=post).aggregate(Count('id'))
            )['id__count']
            PostReport.objects.create(
                post_id=post,
                report_reason=reason,
                report_date=dt.datetime.now(),
                report_count=report_count + 1
            )

    else:
        form = ReportForm()

    return render(
        request,
        'kuhub/report_post.html',
        {'form': form, 'post': post}
    )
