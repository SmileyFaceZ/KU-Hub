from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from kuhub.models import PostDownload, Post, Tags, Subject
from kuhub.views import SummaryHubView


class TricksHubViewTest(TestCase):

    def setUp(self):
        # Create users for testing
        self.user = User(
            username='testuser',
            password='testpassword'
        )
        self.user.save()

        # Create a post download with tag_id=2 for testing
        self.tag = Tags(tag_text="3")
        self.tag.save()
        self.subject = Subject()
        self.subject.save()

        self.trick_post = Post.objects.create(
                username=self.user,
                post_content='This is a test tricks post',
                tag_id=self.tag,
            )

    def test_tricks_hub_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the summary hub view
        response = self.client.get(reverse('kuhub:tricks'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'kuhub/tricks.html')

        # Check if the correct context variables are present
        self.assertIn('tricks_list', response.context)
        self.assertIn('like_icon_styles', response.context)
        self.assertIn('dislike_icon_styles', response.context)
        self.assertIn('profiles_list', response.context)
        self.assertIn('form', response.context)

        # Check if the summary post download is in the context
        self.assertIn(self.trick_post, response.context['tricks_list'])
