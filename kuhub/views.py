from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from ku_hub.models import *


# Create your views here.

class ReviewHubView(generic.ListView):
    template_name = 'kuhub/review.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Post.objects.order_by('-post_date')


class SummaryHubView(generic.ListView):
    template_name = 'kuhub/summary.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Post.objects.order_by('-post_date')


class TricksHubView(generic.ListView):
    template_name = 'kuhub/tricks.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Post.objects.order_by('-post_date')


class EncouragementView(generic.ListView):
    template_name = 'kuhub/encourage.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Post.objects.order_by('-post_date')

