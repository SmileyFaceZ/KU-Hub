"""Import path from django"""
from django.urls import path
from django.views.generic import RedirectView
from kuhub import views


app_name = "kuhub"
urlpatterns = [
    path('', RedirectView.as_view(url="review-hub/")),
    path('review-hub/', views.ReviewHubView.as_view(), name='review'),
    path('summary-hub/', views.SummaryHubView.as_view(), name='summary'),
    path('tricks-hub/', views.TricksHubView.as_view(), name='tricks'),
    path('encouragement/',
         views.EncouragementView.as_view(),
         name='encouragement'
    ),
    path('liked/', views.like_post, name='like_post'),
    path('disliked/', views.dislike_post, name='dislike_post'),
    path('create-post/', views.create_post, name='create_post'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('toggle-follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
]
