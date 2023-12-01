from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from isp_project import settings
from kuhub.forms import ProfileForm
from kuhub.models import Post, Profile, UserFollower
from django.contrib.auth.models import User
from datetime import timedelta
from django.db.utils import DataError
from kuhub.views.firebase_view import navbar_setting_profile, separate_folder_firebase
from firebase_admin import storage
import os
import re
import logging

LOGGER = logging.getLogger('kuhub')

def profile_view(request, username):
    # Retrieve the user based on the username
    user = get_object_or_404(User, username=username)

    # Retrieve the user's profile
    profile = get_object_or_404(Profile, user=user)

    # Get followers and following counts
    following = UserFollower.objects.filter(user_followed=user)
    followers = UserFollower.objects.filter(follower=user)
    posts_list = Post.objects.filter(username=user).order_by('-post_date')

    # Check if the current user is following the viewed profile
    is_following = False
    if request.user.is_authenticated:
        is_following = request.user.follower.filter(user_followed=user).exists()

    file_store_profile = separate_folder_firebase('profile/')
    for post in posts_list:
        post.username.profile.display_photo = file_store_profile[post.username.profile.display_photo]

    navbar_setting_profile(request)
    profile.display_photo = file_store_profile[profile.display_photo]

    context = {
        'profile': profile,
        'followers_count': following,
        'following_count': followers,
        'is_following': is_following,
        'user': request.user,
        'posts_list': posts_list,
        'like_icon_styles': [post.like_icon_style(request.user) for post in posts_list],
        'dislike_icon_styles': [post.dislike_icon_style(request.user) for post in posts_list],
    }

    return render(request, 'kuhub/profile.html', context)

@login_required
def profile_settings(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            try:
                form.save()
                display_photo_url = request.POST.get('display_photo_url')

                if display_photo_url:
                    profile.display_photo = display_photo_url
                    profile.save()

                    clean_file_name = re.sub(r'\s+', '_', display_photo_url)
                    clean_file_name = re.sub(r'[()]', '', clean_file_name)
                    clean_file_path = os.path.join(settings.MEDIA_ROOT,
                                                   clean_file_name)

                    if os.path.exists(clean_file_path):
                        os.remove(clean_file_path)

                messages.success(request, 'Profile updated successfully!')
            except DataError as e:
                LOGGER.error(
                    f'Error updating profile for user {user.username}: {e}')
                messages.warning(request,
                               'Error updating profile. The file name might be too long. Please try a shorter file name.')
            return redirect('kuhub:profile_settings')

    else:
        form = ProfileForm(instance=profile)

    following = UserFollower.objects.filter(user_followed=user)
    followers = UserFollower.objects.filter(follower=user)
    biography = Profile.objects.filter(biography=profile.biography)

    bucket = storage.bucket()
    blobs = bucket.list_blobs(prefix='profile/')
    file_store = {}

    for blob in blobs:
        # Generate a signed URL for each file
        if not blob.name.endswith('/'):
            signed_url = blob.generate_signed_url(
                expiration=timedelta(seconds=300))
            delete_folder = blob.name.replace('profile/', '')
            file_store[delete_folder] = signed_url

    # Change file name into url
    try:
        profile.display_photo = file_store[profile.display_photo]
    except KeyError:
        Profile.objects.filter(user=user).update(display_photo='default_profile_picture.png')
        update_profile = Profile.objects.get(user=user)
        profile.display_photo = file_store[update_profile.display_photo]

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
