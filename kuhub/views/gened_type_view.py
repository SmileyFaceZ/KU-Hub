"""Module to represent a list of all subject type from database."""
from django.contrib import messages
from django.http import HttpRequest, Http404
from django.views import generic
from kuhub.models import Subject
from kuhub.filters import GenedFilter
from django.shortcuts import get_object_or_404, render, redirect
from kuhub.models import Post
from kuhub.views.firebase_view import navbar_setting_profile


class GenEdTypeListView(generic.ListView):
    """Redirect to show a type all subject type list."""

    template_name = 'kuhub/gened_list.html'
    context_object_name = 'type_list'

    def get_queryset(self):
        """Return QuerySet of all subjects ordered by course_code."""
        tag_list = (Subject.objects.values_list("type", flat=True)
                    .distinct().order_by('type'))
        return [tag.replace("_", " ") for tag in tag_list]

    def get_context_data(self, **kwargs):
        """Return user'group data as contect data."""
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
        navbar_setting_profile(request)
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

