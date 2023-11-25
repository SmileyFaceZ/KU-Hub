import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from kuhub.models import Post, PostReport, Tags, Subject


class PostReportModelTests(TestCase):

    def setUp(self):
        # Create a user and post for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.tag = Tags()
        self.tag.save()
        self.subject = Subject()
        self.subject.save()
        self.post1 = Post.objects.create(
            username=self.user,
            post_content="Test post.",
            tag_id=self.tag,
            subject=self.subject
        )
        self.post2 = Post.objects.create(
            username=self.user,
            post_content="Test post 2.",
            tag_id=self.tag,
            subject=self.subject
        )

    # def test_number_of_report(self):
    #     report_1 = PostReport(
    #         post_id=self.post1,
    #         report_reason="test report"
    #     )
    #     report_1.save()
    #     report_2 = PostReport(
    #         post_id=self.post1,
    #         report_reason="test report 2"
    #     )
    #     report_2.save()
    #     self.assertEqual(report_2.report_count, 1)

    def test_report_post_relationship(self):
        """
        post_id should establish a ForeignKey relationship with the Post model.
        """
        report = PostReport(
            post_id=self.post1,
            report_reason="Inappropriate content."
        )
        report.save()
        self.assertEqual(report.post_id, self.post1)
