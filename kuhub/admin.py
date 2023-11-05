"""Import admin class from django"""
from django.contrib import admin
from kuhub.models import \
    UserFollower, Post, PostComments, Tags, PostDownload, PostReport

# Register your models here.

admin.site.register(UserFollower)
admin.site.register(Post)
admin.site.register(PostComments)
admin.site.register(Tags)
admin.site.register(PostDownload)
admin.site.register(PostReport)
