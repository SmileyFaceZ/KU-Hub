import django_filters
from kuhub.models import Post
from django import forms


class PostFilter(django_filters.FilterSet):
    LIKED_DISLIKED_CHOICE = [
        ('', 'Any'),
        ('asc', 'Most Liked'),
        ('desc', 'Most Disliked'),
    ]

    POST_CHOICES = [
        ('', 'Any'),
        ('asc', 'Recent'),
        ('desc', 'Oldest'),
    ]

    pose_content = django_filters.CharFilter(
        label='Post Content',
        field_name='post_content',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    order_by_liked_disliked = django_filters.ChoiceFilter(
        label='Order by Like or Dislike',
        choices=LIKED_DISLIKED_CHOICE,
        method='filter_by_liked_disliked',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    order_by_post = django_filters.ChoiceFilter(
        label='Order by Post',
        choices=POST_CHOICES,
        method='filter_by_post',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def filter_by_liked_disliked(self, queryset, name, value):
        """Return queryset ordered by liked or disliked."""
        if value == 'asc':
            return queryset.order_by('-liked')
        elif value == 'desc':
            return queryset.order_by('-disliked')
        return queryset

    def filter_by_post(self, queryset, name, value):
        """Return queryset ordered by post."""
        if value == 'asc':
            return queryset.order_by('-post_date')
        elif value == 'desc':
            return queryset.order_by('post_date')
        return queryset
