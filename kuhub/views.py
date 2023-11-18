"""
Contains view functions for handling requests.
related to Review-Hub, Summary-Hub and Tricks-Hub
in the kuhub web application.
"""
import datetime

from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import TemplateView
import json
import datetime as dt
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from kuhub.forms import PostForm, ProfileForm, GroupForm
from kuhub.models import Post, PostDownload, Tags, Profile, UserFollower, Group, GroupTags, GroupPassword
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .calendar import get_google_calendar_service, create_event,create_calendar

class ReviewHubView(generic.ListView):
    """Redirect to Review-Hub page for review posts."""

    template_name: str = 'kuhub/review.html'
    context_object_name: str = 'posts_list'

    def get_queryset(self) -> QuerySet[Post]:
        """Return Post objects with tag_id=1 and order by post_date."""
        return Post.objects.filter(tag_id=1).order_by('-post_date')

    def get_context_data(self, **kwargs):
        """Add like and dislike icon styles to context."""
        context = super().get_context_data(**kwargs)
        context['like_icon_styles'] = [post.like_icon_style(self.request.user)
                                       for post in context['posts_list']]
        context['dislike_icon_styles'] = [
            post.dislike_icon_style(self.request.user) for post in
            context['posts_list']]
        return context


class SummaryHubView(generic.ListView):
    """Redirect to Summary-Hub page for summary posts."""

    template_name: str = 'kuhub/summary.html'
    context_object_name: str = 'summary_post_list'

    def get_queryset(self) -> QuerySet[PostDownload]:
        """Return PostDownload objects with tag_id=2 and order by post_date."""
        return PostDownload.objects.select_related('post_id__tag_id').order_by(
            '-post_id__post_date'
        ).all()

    def get_context_data(self, **kwargs):
        """Add like and dislike icon styles to context."""
        context = super().get_context_data(**kwargs)
        context['like_icon_styles'] = [post.like_icon_style(self.request.user)
                                       for post in context['summary_post_list']]
        context['dislike_icon_styles'] = [
            post.dislike_icon_style(self.request.user) for post in
            context['summary_post_list']]
        return context


class TricksHubView(generic.ListView):
    """Redirect to Tricks-Hub page for tricks posts."""

    template_name: str = 'kuhub/tricks.html'
    context_object_name: str = 'tricks_list'

    def get_queryset(self) -> QuerySet[Post]:
        """Return Post objects with tag_id=3 and order by post_date."""
        return Post.objects.filter(tag_id=3).order_by('-post_date')

    def get_context_data(self, **kwargs):
        """Add like and dislike icon styles to context."""
        context = super().get_context_data(**kwargs)
        context['like_icon_styles'] = [post.like_icon_style(self.request.user)
                                       for post in context['tricks_list']]
        context['dislike_icon_styles'] = [
            post.dislike_icon_style(self.request.user) for post in
            context['tricks_list']]
        return context


class GroupView(generic.ListView):
    """
    Redirect to Group-Hub page.
    """
    template_name = 'kuhub/group.html'
    context_object_name = 'group_list'

    def get_queryset(self):
        """Return most 100 recent group posts."""
        return Group.objects.all().order_by('-create_date')[:100]

    def get_context_data(self, **kwargs):
        """Return user'group data as contect data"""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_groups'] = self.request.user.group_set.all()
        return context

@login_required
def join(request,group_id):
    """
    Join Group button
    """
    user = request.user
    group = get_object_or_404(Group,pk=group_id)
    if user in group.group_member.all():
        messages.error(request, "You already a member of this group")
        return redirect(reverse('kuhub:groups'))
    if group.group_password:
        if request.method == 'POST':
            password = request.POST['pass']
            if not group.group_password.check_password(password):
                messages.error(request, "Wrong password")
                return redirect(reverse('kuhub:groups'))
    group.group_member.add(user)
    messages.success(request, "You join the group success!")
    return redirect(reverse('kuhub:groups'))

@login_required
def create_group(request: HttpRequest):
    """
    Create Group
    """
    user = request.user
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            #check password and password(again) is the same
            if data['password'] != data['password_2'] :
                messages.error(request, "Password is not the same")
                return render(
                    request,
                    template_name='kuhub/group_create.html',
                    context={'form': GroupForm}
                )
            # if not have the tag in groupTag object create it
            group_tag, created = GroupTags.objects.get_or_create(tag_text=data['tag_name'])
            # create group object
            password = None
            if data['password']:
                password = GroupPassword.objects.create(group_password=data['password'])
                password.set_password(password.group_password)
            calendar = create_calendar("calendar")
            group = Group.objects.create(
                group_name=data['name'],
                group_description=data['description'],
                group_password=password,
                group_calendar=calendar['id']
            )
            group.group_tags.set([group_tag])
            group.group_member.set([user])
            messages.success(request, f'Create group successful your group id is {group.id}')
            return redirect(reverse('kuhub:groups'))
    return render(
        request,
        template_name='kuhub/group_create.html',
        context={'form': GroupForm}
    )

@method_decorator(login_required, name='dispatch')
class GroupDetail(generic.DetailView):
    """Group manage and detail page"""
    model = Group
    template_name = 'kuhub/group_detail.html'

    def get_queryset(self):
        return Group.objects.all()



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


@login_required
def profile_settings(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('kuhub:profile_settings')

    else:
        form = ProfileForm(instance=profile)

    following = UserFollower.objects.filter(user_followed=user)
    followers = UserFollower.objects.filter(follower=user)
    biography = Profile.objects.filter(biography=profile.biography)

    return render(request,
                  template_name='kuhub/profile_settings.html',
                  context={
                      'form': form,
                      'user': user,
                      'profile': profile,
                      'following': following,
                      'followers': followers,
                      'biography': biography
                  })


def profile_view(request, username):

    # Retrieve the user based on the username
    user = get_object_or_404(User, username=username)

    # Retrieve the user's profile
    profile = get_object_or_404(Profile, user=user)

    # Get followers and following counts
    following = UserFollower.objects.filter(user_followed=user)
    followers = UserFollower.objects.filter(follower=user)
    posts_list = Post.objects.filter(username=user)

    # Check if the current user is following the viewed profile
    is_following = False
    if request.user.is_authenticated:
        is_following = request.user.follower.filter(user_followed=user).exists()

    context = {
        'profile': profile,
        'followers_count': following,
        'following_count': followers,
        'is_following': is_following,
        'user': request.user,
        'posts_list': posts_list,
    }

    return render(request, 'kuhub/profile.html', context)


@login_required
@require_POST
def toggle_follow(request, user_id):
    user_to_follow = User.objects.get(pk=user_id)
    follower = request.user

    is_following = UserFollower.objects.filter(user_followed=user_to_follow, follower=follower).exists()

    if is_following:
        # If already following, unfollow
        UserFollower.objects.filter(user_followed=user_to_follow, follower=follower).delete()
    else:
        # If not following, follow
        UserFollower.objects.create(user_followed=user_to_follow, follower=follower)

    # Recalculate counts
    followers_count = UserFollower.objects.filter(user_followed=user_to_follow).count()

    return JsonResponse({'is_following': not is_following, 'followers_count': followers_count})


@login_required
def followers_page(request):
    user = request.user
    followers = UserFollower.objects.filter(user_followed=user)

    return render(request, "kuhub/followers_page.html", context={'followers': followers})


@login_required
def following_page(request):
    user = request.user
    following = UserFollower.objects.filter(follower=user)

    return render(request, "kuhub/following_page.html", context={'followings': following})

