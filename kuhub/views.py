"""
Contains view functions for handling requests.
related to Review-Hub, Summary-Hub and Tricks-Hub
in the kuhub web application.
"""
from django.utils.decorators import method_decorator
from django.http import Http404
import json
import datetime as dt
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet, Count
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from kuhub.forms import EventForm
from .calendar import create_event
from kuhub.forms import PostForm, ProfileForm, GroupForm, CommentForm, ReportForm
from kuhub.models import (Post, PostDownload, Tags, Profile, UserFollower, PostReport,
                          Group, GroupTag, GroupPassword, Subject, PostComments, GroupEvent, Note)
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from kuhub.filters import PostFilter, PostDownloadFilter, GenedFilter


class HomePageView(generic.ListView):
    template_name = 'kuhub/home_page.html'
    context_object_name: str = 'followed_users_posts'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            messages.info(self.request, "Please login first")
            return Post.objects.none()

        followed_users = UserFollower.objects.filter(follower=self.request.user).values_list('user_followed', flat=True)
        followed_users_posts = Post.objects.filter(user__in=followed_users).order_by('-post_date')

        if not followed_users.exists():
            return followed_users_posts.none()

        self.filterset = PostFilter(self.request.GET, queryset=followed_users_posts)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Add like and dislike icon styles and search form to context."""
        context = super().get_context_data(**kwargs)

        # Check if the user is authenticated
        if self.request.user.is_authenticated:
            followed_users = UserFollower.objects.filter(follower=self.request.user).values_list('user_followed',
                                                                                                 flat=True)
            followed_users_posts = Post.objects.filter(user__in=followed_users).order_by('-post_date')

            # Check if the user is following anyone
            if not followed_users.exists():
                messages.info(self.request, "You are not following anyone yet.")

            queryset = followed_users_posts
            self.filterset = PostFilter(self.request.GET, queryset=queryset)
            context['followed_users_posts'] = self.filterset.qs
            context['like_icon_styles'] = [post.like_icon_style(self.request.user) for post in
                                           context['followed_users_posts']]
            context['dislike_icon_styles'] = [post.dislike_icon_style(self.request.user) for post in
                                              context['followed_users_posts']]

        else:
            # User is not authenticated, display a message
            messages.info(self.request, "Please log in to see posts from people you follow.")

            # Provide an empty queryset to prevent errors
            context['followed_users_posts'] = Post.objects.none()

        # Include search form in the context
        context['form'] = getattr(self, 'filterset', None) and getattr(self.filterset, 'form', None)

        # Include profiles list in the context
        context['profiles_list'] = [Profile.objects.filter(user=post.user).first() for post in
                                    context['followed_users_posts']]

        return context


class ReviewHubView(generic.ListView):
    """Redirect to Review-Hub page for review posts."""
    queryset = Post.objects.all().filter(tag_id=1).order_by('-post_date')
    template_name: str = 'kuhub/review.html'
    context_object_name: str = 'posts_list'

    def get_queryset(self) -> QuerySet[Post]:
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Add like and dislike icon styles to context."""
        context = super().get_context_data(**kwargs)

        profiles_list = [Profile.objects.filter(user=post.user).first()
                         for post in context['posts_list']]

        context['like_icon_styles'] = [post.like_icon_style(self.request.user)
                                       for post in context['posts_list']]
        context['dislike_icon_styles'] = [
            post.dislike_icon_style(self.request.user) for post in
            context['posts_list']]
        context['profiles_list'] = profiles_list
        context['form'] = self.filterset.form

        return context


class SummaryHubView(generic.ListView):
    """Redirect to Summary-Hub page for summary posts."""

    queryset = ((PostDownload.objects
                 .select_related('post_id__tag_id'))
                .order_by('-post_id__post_date').all())
    template_name: str = 'kuhub/summary.html'
    context_object_name: str = 'summary_post_list'

    def get_queryset(self) -> QuerySet[PostDownload]:
        """Return PostDownload objects with tag=2 and order by post_date."""
        queryset = super().get_queryset()
        self.filterset = PostDownloadFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Add like and dislike icon styles to context."""
        context = super().get_context_data(**kwargs)

        profiles_list = [Profile.objects.filter(user=post.post.user).first()
                         for post in context['summary_post_list']]

        context['like_icon_styles'] = [post.like_icon_style(self.request.user)
                                       for post in context['summary_post_list']]
        context['dislike_icon_styles'] = [
            post.dislike_icon_style(self.request.user) for post in
            context['summary_post_list']]
        context['profiles_list'] = profiles_list
        context['form'] = self.filterset.form

        return context


class TricksHubView(generic.ListView):
    """Redirect to Tricks-Hub page for tricks posts."""

    queryset = Post.objects.filter(tag_id=3).order_by('-post_date')
    template_name: str = 'kuhub/tricks.html'
    context_object_name: str = 'tricks_list'

    def get_queryset(self) -> QuerySet[Post]:
        """Return Post objects with tag=3 and order by post_date."""
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Add like and dislike icon styles to context."""
        context = super().get_context_data(**kwargs)

        profiles_list = [Profile.objects.filter(user=post.user).first()
                         for post in context['tricks_list']]

        context['like_icon_styles'] = [post.like_icon_style(self.request.user)
                                       for post in context['tricks_list']]
        context['dislike_icon_styles'] = [
            post.dislike_icon_style(self.request.user) for post in
            context['tricks_list']]
        context['profiles_list'] = profiles_list
        context['form'] = self.filterset.form

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


class GenEdTypeListView(generic.ListView):
    """Redirect to show a type all subject type list."""
    template_name = 'kuhub/gened_list.html'
    context_object_name = 'type_list'

    def get_queryset(self):
        """Return QuerySet of all subjects ordered by course_code"""
        tag_list = (Subject.objects.values_list("type", flat=True)
                    .distinct().order_by('type'))
        return [tag.replace("_", " ") for tag in tag_list]

    def get_context_data(self, **kwargs):
        """Return user'group data as contect data"""
        context = super().get_context_data(**kwargs)
        subject_list = Subject.objects.all().order_by('course_code')

        subject_filter = GenedFilter(
            self.request.GET,
            queryset=subject_list
        )
        for subject in subject_filter.qs:
            subject.type = subject.type.replace("_", " ")

        context['subject_list'] = subject_filter.qs
        for i in subject_filter.qs:
            print(i.type)
        context['form'] = subject_filter.form

        return context


class SubjectDetailView(generic.ListView):
    """Redirect to review and summary detail of each subject page."""
    template_name = 'kuhub/subject_detail.html'
    context_object_name = 'subject_detail'

    def get(self, request: HttpRequest, **kwargs):
        try:
            key = kwargs["course_code"]
            subject = get_object_or_404(Subject, course_code=key)
        except Http404:
            messages.warning(
                request,
                f"Subject Course Code {key} does not exist.❗️")
            return redirect("kuhub:gen_ed_type_list")

        course_code_post = [
            post for post in Post.objects.all().order_by('-post_date')
            if key == post.subject.course_code
        ]

        return render(
            request,
            'kuhub/subject_detail.html',
            context={
                "course_code_post": course_code_post,
                "subject": subject.course_code + " " + subject.name_eng,
            }
        )


@login_required
def join(request, group_id):
    """
    Join Group button
    """
    user = request.user
    group = get_object_or_404(Group, pk=group_id)
    # if not user.email:
    #     messages.error(request, "Please add email in your profile")
    #     return redirect(reverse('kuhub:groups'))

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
            # check password and password(again) is the same
            if data['password'] != data['password_2']:
                messages.error(request, "Password is not the same")
                return render(
                    request,
                    template_name='kuhub/group_create.html',
                    context={'form': GroupForm}
                )
            # if not have the tag in groupTag object create it
            group_tag, created = GroupTag.objects.get_or_create(tag_text=data['tag_name'])
            # create group object
            password = None
            if data['password']:
                password = GroupPassword.objects.create(group_password=data['password'])
                password.set_password(password.group_password)
            group = Group.objects.create(
                group_name=data['name'],
                group_description=data['description'],
                group_password=password,
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

    def get_context_data(self, **kwargs):
        """Return user'group data as contect data"""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['events'] = self.object.groupevent_set.all()
            context['notes'] = self.object.note_set.all()
        return context


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
            post_obj = get_object_or_404(Post, id=js_post['post'])

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
            post_obj: Post = get_object_or_404(Post, id=js_post['post'])

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
            print('data', data)

            post = Post.objects.create(
                user=request.user,
                post_content=data['review'],
                post_date=dt.datetime.now(),
                subject=Subject.objects.get(course_code=data['subject']),
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
            messages.success(request, 'Changed successfully!')
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
    # Retrieve the user based on the user
    user = get_object_or_404(User, username=username)

    # Retrieve the user's profile
    profile = get_object_or_404(Profile, user=user)

    # Get followers and following counts
    following = UserFollower.objects.filter(user_followed=user)
    followers = UserFollower.objects.filter(follower=user)
    posts_list = Post.objects.filter(user=user).order_by('-post_date')

    # Check if the current user is following the viewed profile
    is_following = False
    if request.user.is_authenticated:
        is_following = request.user.follower.filter(user_followed=user).exists()

    like_icon_styles = [post.like_icon_style(request.user)
                        for post in posts_list]
    dislike_icon_styles = [post.dislike_icon_style(request.user)
                           for post in posts_list]

    context = {
        'profile': profile,
        'followers_count': following,
        'following_count': followers,
        'is_following': is_following,
        'user': request.user,
        'posts_list': posts_list,
        'like_icon_styles': like_icon_styles,
        'dislike_icon_styles': dislike_icon_styles
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


def group_event_create(request, group_id):
    user = request.user
    is_google_user = user.socialaccount_set.filter(provider='google').exists()
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            meet_link = ''
            group_event = GroupEvent.objects.create(
                group=group,
                summary=data['summary'],
                location=data['location'],
                description=data['description'],
                start_time=data['start_time'].strftime('%Y-%m-%dT%H:%M:%S'),
                end_time=data['end_time'].strftime('%Y-%m-%dT%H:%M:%S'),
                show_time=f"{data['start_time'].strftime('%a. %d %b %Y %H:%M:%S')} - {data['end_time'].strftime('%a. %d %b %Y %H:%M:%S')}"
            )
            if data['is_meeting']:
                try:
                    event, meet_link = create_event(request=request,
                                                    summary=data['summary'],
                                                    description=data['description'],
                                                    location=data['location'],
                                                    start_datetime=data['start_time'].strftime('%Y-%m-%dT%H:%M:%S'),
                                                    end_datetime=data['end_time'].strftime('%Y-%m-%dT%H:%M:%S'))
                except:
                    messages.error(request, "You have to login with google before using this feature")
                    return redirect(reverse('kuhub:group_detail', args=(group_id,)))
            group_event.link = str(meet_link)
            group_event.save()
            messages.success(request, f'create event successful')
            return redirect(reverse('kuhub:group_detail', args=(group_id,)))
    return render(
        request,
        template_name='kuhub/group_event.html',
        context={'form': EventForm, 'group': group, 'user': user, 'is_google': is_google_user}
    )


def group_event_delete(request, event_id):
    user = request.user
    event = get_object_or_404(GroupEvent, pk=event_id)
    group_id = event.group.id
    # delete GroupEvent object
    event.delete()
    messages.success(request, 'delete event successful')
    return redirect(reverse('kuhub:group_detail', args=(group_id,)))


def add_note(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        text = request.POST.get('note', '')
        Note.objects.create(group=group, note_text=text)
        messages.success(request, 'create note successful')
        return redirect(reverse('kuhub:group_detail', args=(group_id,)))


def delete_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    group_id = note.group.id
    note.delete()
    messages.success(request, 'delete note successful')
    return redirect(reverse('kuhub:group_detail', args=(group_id,)))


# views.py
from django.shortcuts import render
from itertools import zip_longest  # Import zip_longest for handling different lengths


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments_list = PostComments.objects.filter(post_id=post)

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)

            if form.is_valid():
                data = form.cleaned_data['comment']
                PostComments.objects.create(user=request.user,
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

    owner_profile = Profile.objects.filter(user=post.user)
    comments_profiles = [Profile.objects.filter(user=comment.user).first()
                         for comment in comments_list]
    like_icon_styles = post.like_icon_style(request.user)
    dislike_icon_styles = post.dislike_icon_style(request.user)

    # Use zip_longest to handle different lengths
    comments_and_profiles = zip_longest(comments_list, comments_profiles)

    context = {
        'post': post,
        'comments_and_profiles': comments_and_profiles,
        'form': form,
        'owner_profile': owner_profile,
        'like_icon_styles': like_icon_styles,
        'dislike_icon_styles': dislike_icon_styles
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

    if request.user != post.user:
        print('do this')
        messages.warning(
            request,
            f"You are not the owner of this post.❗️"
        )

        return redirect('kuhub:post_detail', pk=post.pk)

    if request.method == "POST":
        print('xxxxxxx')
        form = PostForm(request.POST)
        if form.is_valid():
            tag_name = form.cleaned_data['tag_name']

            tag = get_object_or_404(Tags, tag_text=tag_name)
            post.tag = tag

            subject_code = form.cleaned_data['subject']
            subject = get_object_or_404(Subject, course_code=subject_code)
            post.subject = subject

            post.post_content = form.cleaned_data['review']

            post.save()

            return redirect('kuhub:post_detail', pk=post.pk)
    else:
        form = PostForm(
            initial={'tag_name': post.tag.tag_text,
                     'subject': post.subject.course_code,
                     'review': post.post_content}
        )

    context = {'form': form, 'user': request.user, 'post': post}
    return render(request, 'kuhub/edit_post.html', context)


def report_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            report_count = PostReport.objects.filter(post_id=post).aggregate(Count('id'))['id__count']
            PostReport.objects.create(post_id=post,
                                      report_reason=reason,
                                      report_date=dt.datetime.now(),
                                      report_count=report_count + 1)
            messages.success(request, 'Report successfully!')
            form = ReportForm()

    else:
        form = ReportForm()

    return render(request, 'kuhub/report_post.html', {'form': form, 'post': post})
