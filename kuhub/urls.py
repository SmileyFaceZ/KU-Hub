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
    path('group-hub/',
         views.GroupView.as_view(),
         name='groups'
    ),
    path('<int:pk>/group', views.GroupDetail.as_view(), name='group_detail'),
    path('<int:group_id>/group-event-create', views.group_event_create, name='group_event'),
    path('<int:group_id>/note',views.add_note, name='group_note'),
    path('<int:note_id>/note/delete',views.delete_note, name='note_delete'),
    path('<int:event_id>/delete',views.group_event_delete, name='event_delete'),
    path('create-group/', views.create_group, name='create_group'),
    path('<int:group_id>/join',views.join,name='join'),
    path('liked/', views.like_post, name='like_post'),
    path('disliked/', views.dislike_post, name='dislike_post'),
    path('create-post/', views.create_post, name='create_post'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('toggle-follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('followers/', views.followers_page, name='followers_page'),
    path('following/', views.following_page, name='following_page'),
    path('gen-ed-list/', views.GenEdTypeListView.as_view(), name='gen_ed_type_list'),
    path('subject/<str:course_code>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('report/<int:pk>/', views.report_post, name='report_post'),
]