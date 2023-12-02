"""Module for display a list of all subject and information of each subject."""
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpRequest, Http404
from django.contrib import messages
from kuhub.models import Subject, Post
from kuhub.views.profile.profile_setting import ProfileSetting
from kuhub.views.firebase_folder import FirebaseFolder


class SubjectDetailView(generic.ListView):
    """Display to review and summary detail of each subject page."""

    template_name = 'kuhub/subject_detail.html'
    context_object_name = 'subject_detail'

    def get(self, request: HttpRequest, **kwargs):
        """Get a type of gen-ed and display all subject in that type."""
        # Display Profile in Navbar
        ProfileSetting.update_display_photo(
            profile=request.user.profile,
            firebase_folder='profile/',
            user=request.user
        )

        try:
            key = kwargs["course_code"]
            subject = get_object_or_404(
                Subject,
                course_code=kwargs["course_code"]
            )
        except Http404:
            messages.warning(
                request,
                f"Subject Course Code {key} does not exist.❗️")
            return redirect("kuhub:gen_ed_type_list")

        course_code_post = [
            post for post in Post.objects.all().order_by('-post_date')
            if key == post.subject.course_code
        ]

        file_store_profile = (
            FirebaseFolder.separate_folder_firebase('profile/'))

        # Change file name into url
        for post in course_code_post:
            post.username.profile.display_photo = (
                file_store_profile)[post.username.profile.display_photo]

        return render(
            request,
            'kuhub/subject_detail.html',
            context={
                "course_code_post": course_code_post,
                "subject": subject.course_code + " " + subject.name_eng,
            }
        )
