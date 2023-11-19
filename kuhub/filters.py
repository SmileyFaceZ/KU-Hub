import django_filters
from django import forms


class PostFilter(django_filters.FilterSet):

    LIKED_DISLIKED_CHOICE = [
        ('asc', 'Most Liked'),
        ('desc', 'Most Disliked'),
    ]

    POST_CHOICES = [
        ('asc', 'Recent'),
        ('desc', 'Oldest'),
    ]

    post_content = django_filters.CharFilter(
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


class PostDownloadFilter(PostFilter):
    """Filter for post download that inherit from PostFilter."""

    POST_DOWNLOAD_CHOICES = [
        ('asc', 'Most Download'),
        ('desc', 'Least Download'),
    ]

    post_content = django_filters.CharFilter(
        label='Post Content',
        field_name='post_id__post_content',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


    order_by_download = django_filters.ChoiceFilter(
        label='Order by Download',
        choices=POST_DOWNLOAD_CHOICES,
        method='filter_by_download',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def filter_by_liked_disliked(self, queryset, name, value):
        """Return queryset ordered by liked or disliked."""
        if value == 'desc':
            return queryset.order_by('-post_id__liked')
        elif value == 'asc':
            return queryset.order_by('-post_id__disliked')
        return queryset

    def filter_by_post(self, queryset, name, value):
        """Return queryset ordered by post."""
        if value == 'asc':
            return queryset.order_by('-post_id__post_date')
        elif value == 'desc':
            return queryset.order_by('post_id__post_date')
        return queryset

    def filter_by_download(self, queryset, name, value):
        """Return queryset ordered by download."""
        if value == 'asc':
            return queryset.order_by('-download')
        elif value == 'desc':
            return queryset.order_by('download')
        return queryset


class PostTrickFilter(django_filters.FilterSet):

    LIKED_DISLIKED_CHOICE = [
        ('asc', 'Most Liked'),
        ('desc', 'Most Disliked'),
    ]

    POST_CHOICES = [
        ('asc', 'Recent'),
        ('desc', 'Oldest'),
    ]

    post_content = django_filters.CharFilter(
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
        print('value', value)
        """Return queryset ordered by liked or disliked."""
        if value == 'desc':
            print('order by liked')
            return queryset.order_by('-liked')
        elif value == 'asc':
            print('order by disliked')
            return queryset.order_by('-disliked')

        return queryset

    def filter_by_post(self, queryset, name, value):
        """Return queryset ordered by post."""
        if value == 'asc':
            return queryset.order_by('-post_date')
        elif value == 'desc':
            return queryset.order_by('post_date')
        return queryset