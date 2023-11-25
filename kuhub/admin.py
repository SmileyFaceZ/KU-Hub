"""Import admin class from django"""
from django.contrib import admin
from kuhub.models import UserFollower, Post, PostComment, Tag, PostDownload, PostReport, \
    Subject, Profile, Group, GroupPassword, GroupTag, GroupEvent


admin.site.register(UserFollower)
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(Tag)
admin.site.register(PostDownload)
admin.site.register(PostReport)
admin.site.register(GroupTag)
admin.site.register(Group)
admin.site.register(GroupPassword)
admin.site.register(Subject)
admin.site.register(Profile)
admin.site.register(GroupEvent)

