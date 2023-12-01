from .firebase_view import separate_folder_firebase, navbar_setting_profile
from .base_view import HomePageView, ReviewHubView, TricksHubView, SummaryHubView
from .follower_view import followers_page, following_page, toggle_follow
from .profile_view import profile_view, profile_settings
from .post_view import post_detail, create_post, edit_post, dislike_post, like_post, report_post
from .gened_type_view import GenEdTypeListView, SubjectDetailView
from .group_view import GroupView, join, create_group
from .group_detail_view import GroupDetail, add_note, delete_note
from .group_event_view import EventDetail, group_event_create, group_event_delete
from .group_task_view import add_task, delete_task, assign_task_in_event, unassign_task, change_task_status