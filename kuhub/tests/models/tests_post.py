import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from kuhub.models import Post, Tag, Subject


class PostModelTests(TestCase):
    def setUp(self) -> None:
        """Set up objects for tests."""
        self.user = User.objects.create_user(username="user", password="password")
        self.tag = Tag()
        self.tag.save()
        self.subject = Subject()
        self.subject.save()
        self.post = Post(
            username=self.user,
            post_content="recent post",
            post_date=timezone.now(),
            tag_id=self.tag,
            subject=self.subject
        )

    def test_was_published_with_future_post(self):
        """Method was_published_recently should return false when with future posts."""
        future_post = Post(
            username=self.user,
            post_content="future post",
            post_date=timezone.now() + datetime.timedelta(days=30),
            tag_id=Tag(),
            subject=Subject()
        )
        self.assertIs(future_post.was_published_recently_post(), False)

    def test_was_published_with_old_post(self):
        """Method was_published_recently should return false when with old posts."""
        old_post = Post(
            username=self.user,
            post_content="old post",
            post_date=timezone.now() - datetime.timedelta(days=30),
            tag_id=Tag(),
            subject=Subject()
        )
        self.assertIs(old_post.was_published_recently_post(), False)

    def test_was_published_with_recent_post(self):
        """Method was_published_recently should return true when with recent posts."""
        recent_post = Post(
            username=self.user,
            post_content="recent post",
            post_date=timezone.now(),
            tag_id=Tag(),
            subject=Subject()
        )
        self.assertIs(recent_post.was_published_recently_post(), True)

    def test_total_likes(self):
        self.post.save()
        self.post.liked.add(self.user)
        self.assertEqual(self.post.total_likes(), 1)

    def test_total_dislikes(self):
        self.post.save()
        self.post.disliked.add(self.user)
        self.assertEqual(self.post.total_dislikes(), 1)
