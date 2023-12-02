"""This module contains views follower and following in the application."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from kuhub.models import UserFollower
from kuhub.views import FirebaseFolder, ProfileSetting
from django.http import HttpRequest, HttpResponse


class FollowView:
    """To handle views related to followers and following."""

    @staticmethod
    def update_display_photo(follows: UserFollower, type: str):
        """To updates the display photo of followers or following from Firebase.

        :param follows: Queryset of UserFollower objects.
        :param type: Type of the follow, either 'follower' or 'following'.
        """
        file_store_profile = FirebaseFolder.separate_folder_firebase(
            'profile/')
        attribute = 'user_followed' if type == 'following' else 'follower'

        for follow in follows:
            user_profile = getattr(follow, attribute).profile
            user_profile.display_photo = file_store_profile.get(
                user_profile.display_photo,
                user_profile.display_photo
            )

    @staticmethod
    def profile_setting(request: HttpRequest):
        """To sets up the profile settings for a user.

        :param request: The HTTP request object.
        """
        # Display Profile in Navbar
        ProfileSetting.update_display_photo(
            profile=request.user.profile,
            firebase_folder='profile/',
            user=request.user
        )

    @classmethod
    @method_decorator(login_required)
    def followers_page(cls, request: HttpRequest) -> HttpResponse:
        """Return render the followers page.

        :param request: The HTTP request object.
        :return HttpResponse: The rendered followers page.
        """
        FollowView.profile_setting(request)
        followers = UserFollower.objects.filter(user_followed=request.user)
        cls.update_display_photo(followers, 'follower')
        return render(
            request,
            "kuhub/followers_page.html",
            {'followers': followers})

    @classmethod
    @method_decorator(login_required)
    def following_page(cls, request: HttpRequest) -> HttpResponse:
        """Return render the following page.

        :param request: The HTTP request object.
        :return HttpResponse: The rendered following page.
        """
        FollowView.profile_setting(request)
        following = UserFollower.objects.filter(follower=request.user)
        cls.update_display_photo(following, 'following')
        return render(
            request,
            "kuhub/following_page.html",
            {'followings': following})
