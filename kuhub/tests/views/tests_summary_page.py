from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import PostDownload, Profile
from .views import SummaryHubView

class SummaryHubViewTest(TestCase):

    def setUp(self):
        # Create users for testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create a post download with tag_id=2 for testing
        self.summary_post_download = PostDownload.objects.create(
            post_id=Post.objects.create(
                username=self.user,
                content='This is a test summary post',
                tag_id=2
            )
        )

        # Create a profile for the user
        Profile.objects.create(
            user=self.user,
            biography='Test biography',
            display_photo='path/to/test/photo.jpg'
        )

    def test_summary_hub_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the summary hub view
        response = self.client.get(reverse('summary_hub'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'kuhub/summary.html')

        # Check if the correct context variables are present
        self.assertIn('summary_post_list', response.context)
        self.assertIn('like_icon_styles', response.context)
        self.assertIn('dislike_icon_styles', response.context)
        self.assertIn('profiles_list', response.context)
        self.assertIn('form', response.context)

        # Check if the summary post download is in the context
        self.assertIn(self.summary_post_download, response.context['summary_post_list'])

    def test_summary_hub_view_no_authenticated_user(self):
        # Access the summary hub view without logging in
        response = self.client.get(reverse('summary_hub'))

        # Check if the response redirects to the login page
        self.assertRedirects(response, f'/accounts/login/?next={reverse("summary_hub")}')
