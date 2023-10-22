from django.views import generic
from kuhub.models import *


# Create your views here.

class ReviewHubView(generic.ListView):
    template_name = 'kuhub/review.html'

    def get_queryset(self):
        return Post.objects.order_by('-post_date')


class SummaryHubView(generic.ListView):
    template_name = 'kuhub/summary.html'

    def get_queryset(self):
        return Post.objects.order_by('-post_date')


class TricksHubView(generic.ListView):
    template_name = 'kuhub/tricks.html'

    def get_queryset(self):
        return Post.objects.order_by('-post_date')


class EncouragementView(generic.ListView):
    template_name = 'kuhub/encourage.html'

    def get_queryset(self):
        return Post.objects.order_by('-post_date')
