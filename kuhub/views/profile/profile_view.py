"""Module for managing profile views and interactions in the application."""
import logging
from django.db.utils import DataError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, Http404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from kuhub.forms import ProfileForm
from kuhub.models import Post, Profile, UserFollower
from django.contrib.auth.models import User
from kuhub.views.firebase_folder import FirebaseFolder
from kuhub.views.profile.profile_setting import ProfileSetting
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileView(LoginRequiredMixin):
    """View for managing user profiles."""

    def __init__(self, request: HttpRequest):
        """Initialize the ProfileView.

        :param request: HttpRequest object containing metadata
        about the request.
        """
        self.request = request
        self.user = request.user
        self.profile = self.user.profile

    @staticmethod
    @login_required
    def profile_view(request: HttpRequest, username: str) -> HttpResponse:
        """Display the profile page for a given user.

        :param request: HttpRequest object.
        :param username: The username of the user whose
        profile is to be displayed.
        """
        # Display Profile in Navbar
        ProfileSetting.update_display_photo(
            profile=request.user.profile,
            firebase_folder='profile/',
            user=request.user
        )

        try:
            user = get_object_or_404(User, username=username)
            profile = get_object_or_404(Profile, user=user)
        except Http404 as error_message:
            messages.warning("Doesn't have this username profile.")
            logging.getLogger('kuhub').error(error_message)
            return redirect('kuhub:review')

        posts_list = Post.objects.filter(username=user).order_by('-post_date')
        is_following = False
        if request.user.is_authenticated:
            is_following = request.user.follower.filter(
                user_followed=user).exists()

        file_store_profile = FirebaseFolder.separate_folder_firebase(
            'profile/')

        for post in posts_list:
            post.username.profile.display_photo = (
                file_store_profile)[post.username.profile.display_photo]

        # ProfilePhoto(request).display_photo_profile()
        profile.display_photo = file_store_profile[profile.display_photo]

        context = {
            'profile': profile,
            'followers_count': UserFollower.objects.filter(
                user_followed=user),
            'following_count': UserFollower.objects.filter(
                follower=user),
            'is_following': is_following,
            'user': request.user,
            'posts_list': posts_list,
            'like_icon_styles': [post.like_icon_style(request.user) for post in
                                 posts_list],
            'dislike_icon_styles': [post.dislike_icon_style(request.user) for
                                    post
                                    in posts_list],
        }
        return render(
            request,
            'kuhub/profile.html',
            context
        )

    def handle_profile_update(self):
        """Handle updating the user's profile."""
        try:
            form = ProfileForm(
                self.request.POST,
                self.request.FILES,
                instance=self.profile)
            if form.is_valid():
                form.save()
                messages.success(
                    self.request,
                    'Profile updated successfully!')

                FirebaseFolder.file_handling(self.profile.display_photo)
        except DataError as error_message:
            (logging.getLogger('kuhub')
             .error(f'Error updating profile for user '
                    f'{self.user.username}: {error_message}'))
            messages.warning(
                self.request,
                'Error updating profile. Please try a shorter file name.')

    @login_required
    @require_POST
    @staticmethod
    def toggle_follow(request: HttpRequest, user_id: int) -> JsonResponse:
        """Toggle the follow status for a given user.

        :param request: HttpRequest object.
        :param user_id: The ID of the user to follow or unfollow.
        :return: JsonResponse with the updated follow status
        and followers count.
        """
        try:
            user_to_follow = get_object_or_404(User, pk=user_id)
        except Http404 as error_message:
            messages.warning("Your didn't following this user")
            logging.getLogger('kuhub').error(error_message)
            return redirect('kuhub:home')

        follower = request.user

        is_following = UserFollower.objects.filter(
            user_followed=user_to_follow,
            follower=follower
        ).exists()
        if is_following:
            UserFollower.objects.filter(
                user_followed=user_to_follow,
                follower=follower
            ).delete()
        else:
            UserFollower.objects.create(
                user_followed=user_to_follow,
                follower=follower)

        followers_count = UserFollower.objects.filter(
            user_followed=user_to_follow).count()
        return JsonResponse({
            'is_following': not is_following,
            'followers_count': followers_count})
