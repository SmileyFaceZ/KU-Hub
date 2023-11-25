import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from kuhub.models import Post, Tags, Subject, PostComments


class PostCommentModelTests(TestCase):
    """Tests for post comment model."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="user", password="password")
        self.tag = Tags()
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

    def test_comment_post_relationship(self):
        """Post id of comment object should match the post."""
        self.post.save()
        comment = PostComments(
            username=self.user,
            post_id=self.post,
            comment="Test comment"
        )
        comment.save()
        self.assertEqual(comment.post_id, self.post)

    def test_comment_user_relationship(self):
        """User of comment object should match the user."""
        self.post.save()
        comment = PostComments(
            username=self.user,
            post_id=self.post,
            comment="Test comment"
        )
        comment.save()
        self.assertEqual(comment.username, self.user)

    def test_comment_str_representation(self):
        """
        __str__() should return the comment content.
        """
        self.post.save()
        comment = PostComments(
            username=self.user,
            post_id=self.post,
            comment="Test comment."
        )
        self.assertEqual(str(comment), "Test comment.")

    def test_comment_date_custom_value(self):
        """
        comment_date should take the provided value when set explicitly.
        """
        custom_date = datetime.datetime(2023, 1, 1, 12, 0, 0)
        self.post.save()
        comment = PostComments(
            username=self.user,
            post_id=self.post,
            comment="Test comment.",
            comment_date=custom_date
        )
        self.assertEqual(comment.comment_date, custom_date)

