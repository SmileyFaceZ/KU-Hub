from django.http import Http404
import json
import datetime as dt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from itertools import zip_longest
from kuhub.forms import PostForm, CommentForm, ReportForm
from kuhub.models import (Post, PostDownload, Tags, Profile, PostReport,
                          Subject, PostComments)
from django.utils import timezone
from kuhub.views import FirebaseFolder, ProfileSetting


class PostFeature:

    @staticmethod
    def create_post(request: HttpRequest):
        """Create post of each tag type and redirect to each tag page."""
        ProfileSetting.update_display_photo(
            profile=request.user.profile,
            firebase_folder='profile/',
            user=request.user
        )
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data

                post = Post.objects.create(
                    username=request.user,
                    post_content=data['review'],
                    post_date=timezone.now(),
                    subject=Subject.objects.get(
                        course_code=data['subject']),
                    tag_id=Tags.objects.get(tag_text=data['tag_name'])
                )

                messages.success(request, 'Create Post Successfully!')

                return PostFeature.separate_view(data, post, request)

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

    @staticmethod
    def separate_view(data: dict, post: Post, request: HttpRequest):
        if data['tag_name'] == 'Review-Hub':
            return redirect('kuhub:review')

        if data['tag_name'] == 'Summary-Hub':
            uploaded_file = request.FILES.get('file_upload')
            PostDownload.objects.create(
                post_id=post,
                file=uploaded_file,
                download_date=timezone.now(),
                download_count=0,
            )
            # Remove file if it already exists
            if uploaded_file:
                FirebaseFolder.file_handling(uploaded_file.name)

            return redirect('kuhub:summary')

        if data['tag_name'] == 'Tricks-Hub':
            return redirect('kuhub:tricks')

        if data['tag_name'] == 'Encouragement':
            return redirect('kuhub:encourage')

    @staticmethod
    def edit_post(request: HttpRequest, pk: int):
        """User can edit their own post content, tag and subject."""
        # Display Profile in Navbar
        ProfileSetting.update_display_photo(
            profile=request.user.profile,
            firebase_folder='profile/',
            user=request.user
        )
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
                f"You are not the owner of this post.❗️"
            )

            return redirect('kuhub:post_detail', pk=post.pk)

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

                return redirect('kuhub:post_detail', pk=post.pk)
        else:
            form = PostForm(
                initial={'tag_name': post.tag_id.tag_text,
                         'subject': post.subject.course_code,
                         'review': post.post_content}
            )

        context = {'form': form, 'user': request.user, 'post': post}
        return render(request, 'kuhub/edit_post.html', context)

    @staticmethod
    def post_detail(request: HttpRequest, pk: int):
        # Display Profile in Navbar
        ProfileSetting.update_display_photo(
            profile=request.user.profile,
            firebase_folder='profile/',
            user=request.user
        )

        try:
            post = get_object_or_404(Post, pk=pk)
        except Http404:
            messages.warning(request, "Not have this post id!.")
            return redirect('kuhub:review')

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
                    messages.success(request, 'Commented successfully!')

                    # Create new instance form to clear it.
                    form = CommentForm

            else:
                return redirect('account_login')
        else:
            form = CommentForm()

        owner_profile = Profile.objects.filter(user=post.username)
        comments_profiles = [
            Profile.objects.filter(user=comment.username).first()
            for comment in comments_list]

        # Use zip_longest to handle different lengths
        comments_and_profiles = zip_longest(comments_list, comments_profiles)

        post = Post.objects.get(pk=pk)
        file_name = post.username.profile.display_photo
        file = FirebaseFolder.separate_folder_firebase(folder='profile/')
        post.username.profile.display_photo = file[file_name]

        context = {
            'post': post,
            'comments_and_profiles': comments_and_profiles,
            'form': form,
            'owner_profile': owner_profile,
        }

        return render(request, 'kuhub/post_detail.html', context)


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
        # return redirect('kuhub:review')

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
            post_obj: Post = get_object_or_404(
                Post,
                id=js_post['post_id'])

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
def report_post(request: HttpRequest, pk: int):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            report_count = \
            PostReport.objects.filter(post_id=post).aggregate(Count('id'))[
                'id__count']
            PostReport.objects.create(post_id=post,
                                      report_reason=reason,
                                      report_date=dt.datetime.now(),
                                      report_count=report_count + 1)
            messages.success(request, 'Report successfully!')
            form = ReportForm()

    else:
        form = ReportForm()

    return render(request, 'kuhub/report_post.html',
                  {'form': form, 'post': post})
