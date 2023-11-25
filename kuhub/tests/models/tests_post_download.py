import datetime
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from kuhub.models import Post, Tags, PostDownload, Subject


class PostDownloadModel(TestCase):
    """Tests for post download model."""
    def setUp(self) -> None:
        # Create a user, tag, and post for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.tag = Tags()
        self.tag.save()
        self.subject = Subject()
        self.subject.save()
        self.post = Post(
            username=self.user,
            post_content="recent post",
            tag_id=self.tag,
            subject=self.subject
        )
        self.post.save()

    def test_str_representation(self):
        """
        __str__() should return a string representation containing the tag, username, and post content.
        """
        post_download = PostDownload(
            post_id=self.post,
            file='path/to/file.pdf'
        )
        self.assertEqual(
            str(post_download),
            f"{self.tag.tag_text} - {str(self.user)} - {self.post.post_content}"
        )

    def test_default_values(self):
        """
        download_date should have a default value when not provided explicitly.
        download_count should default to 0.
        """
        post_download = PostDownload(
            post_id=self.post,
            file='path/to/file.pdf'
        )
        post_download.save()
        self.assertIsNone(post_download.download_date)
        self.assertEqual(post_download.download_count, 0)

    def test_custom_values(self):
        """
        download_date and download_count should take the provided values when set explicitly.
        """
        custom_date = datetime.datetime(2023, 1, 1, 12, 0, 0)
        post_download = PostDownload(
            post_id=self.post,
            file='path/to/file.pdf',
            download_date=custom_date,
            download_count=5
        )
        post_download.save()
        self.assertEqual(post_download.download_date, custom_date)
        self.assertEqual(post_download.download_count, 5)

    def test_total_likes(self):
        """
        total_likes() should return the total number of likes for the associated post.
        """
        post_download = PostDownload(
            post_id=self.post,
            file='path/to/file.pdf'
        )
        post_download.save()
        self.assertEqual(post_download.total_likes(), self.post.liked.all().count())

    def test_total_dislikes(self):
        """
        total_dislikes() should return the total number of dislikes for the associated post.
        """
        post_download = PostDownload(
            post_id=self.post,
            file='path/to/file.pdf'
        )
        post_download.save()
        self.assertEqual(post_download.total_dislikes(), self.post.disliked.all().count())
