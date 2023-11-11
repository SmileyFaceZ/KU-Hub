"""Import Post and PostDownload models"""
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import TemplateView

from kuhub.models import Post, PostDownload, Group
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse


class ReviewHubView(generic.ListView):
    """
    Redirect to Review-Hub page.
    """
    template_name = 'kuhub/review.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        """Return recently published review posts."""
        return Post.objects.filter(tag_id=1).order_by('-post_date')


class SummaryHubView(generic.ListView):
    """
    Redirect to Summary-Hub page.
    """
    template_name = 'kuhub/summary.html'
    context_object_name = 'summary_post_list'

    def get_queryset(self):
        """Return summary posts queryset."""
        return PostDownload.objects.select_related('post_id__tag_id').all()


class TricksHubView(generic.ListView):
    """
    Redirect to Tricks-Hub page.
    """
    template_name = 'kuhub/tricks.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        """Return recently published trick posts."""
        return Post.objects.filter(tag_id=3).order_by('-post_date')


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


