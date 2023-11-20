from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from kuhub.forms import ProfileForm
from kuhub.models import Post, Profile, UserFollower
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST


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
