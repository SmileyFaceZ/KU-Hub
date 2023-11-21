"""Import admin class from django"""
from django.contrib import admin
from kuhub.models import UserFollower, Post, PostComments, Tags, PostDownload, PostReport, Subject, Profile, Group, GroupPassword, GroupTags, GroupEvent, Notification



# Register your models here.

admin.site.register(UserFollower)
admin.site.register(Post)
admin.site.register(PostComments)
admin.site.register(Tags)
admin.site.register(PostDownload)
admin.site.register(PostReport)
admin.site.register(GroupTags)
admin.site.register(Group)
admin.site.register(GroupPassword)
admin.site.register(Subject)
admin.site.register(Profile)
admin.site.register(GroupEvent)
admin.site.register(Notification)

