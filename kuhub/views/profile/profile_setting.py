import logging
from typing import Dict
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from kuhub.forms import ProfileForm
from kuhub.models import Profile, UserFollower
from kuhub.views.firebase_folder import FirebaseFolder
from django.db import DataError
from django.contrib import messages

LOGGER = logging.getLogger('kuhub')

class ProfileSetting:

    @staticmethod
    def update_display_photo(profile: Profile, firebase_folder: str, user: User) -> Profile:
        try:
            firestore = FirebaseFolder.separate_folder_firebase(firebase_folder)
            profile.display_photo = firestore[profile.display_photo]
        except (KeyError, DataError, AttributeError) as error_message:
            LOGGER.error(f'Error updating display photo: {error_message}')
            user_profile = Profile.objects.filter(user=user).update(
                display_photo='default_profile_picture.png')
            profile.display_photo = firestore[user_profile.display_photo]

    def build_profile_context(self, user: User, form: ProfileForm,
                              profile: Profile) -> Dict[str, any]:
        return {
            'form': form,
            'user': user,
            'profile': profile,
            'following': UserFollower.objects.filter(user_followed=user),
            'followers': UserFollower.objects.filter(follower=user)
        }

    @classmethod
    @method_decorator(login_required)
    def profile_settings(cls, request: HttpRequest) -> render:
        user = request.user
        profile = user.profile

        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, 'Profile updated successfully!')
                except DataError as e:
                    LOGGER.error(f'Error saving profile: {e}')
                    messages.error(request,
                                   'Failed to save profile. Data too long.')
            else:
                messages.error(request, "Form data is not valid.")
        else:
            form = ProfileForm(instance=profile)

        cls.update_display_photo(profile, 'profile/', user)

        context = cls.build_profile_context(
            cls,
            user=user,
            form=form,
            profile=profile)
        return render(request, 'kuhub/profile_settings.html', context)
