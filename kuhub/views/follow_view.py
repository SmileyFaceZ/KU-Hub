from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from kuhub.models import UserFollower
from kuhub.views import FirebaseFolder
from django.http import HttpRequest

class FollowView:

    @staticmethod
    def update_display_photo(follows: UserFollower, type: str):
        file_store_profile = FirebaseFolder.separate_folder_firebase(
            'profile/')
        attribute = 'user_followed' if type == 'following' else 'follower'

        for follow in follows:
            user_profile = getattr(follow, attribute).profile
            user_profile.display_photo = file_store_profile.get(
                user_profile.display_photo,
                user_profile.display_photo
            )

    @classmethod
    @method_decorator(login_required)
    def followers_page(cls, request: HttpRequest):
        followers = UserFollower.objects.filter(user_followed=request.user)
        cls.update_display_photo(followers, 'follower')
        return render(
            request,
            "kuhub/followers_page.html",
            {'followers': followers})

    @classmethod
    @method_decorator(login_required)
    def following_page(cls, request: HttpRequest):
        following = UserFollower.objects.filter(follower=request.user)
        cls.update_display_photo(following, 'following')
        return render(
            request,
            "kuhub/following_page.html",
            {'followings': following})