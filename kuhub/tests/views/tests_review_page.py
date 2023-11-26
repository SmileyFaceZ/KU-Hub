from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from kuhub.models import Post, Profile, Tags, Subject
from kuhub.views import ReviewHubView


class ReviewHubViewTest(TestCase):

    def setUp(self):
        # Create users for testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.tag = Tags()
        self.tag.save()
        self.subject = Subject()
        self.subject.save()

        # Create a post with tag_id=1 for testing
        self.review_post = Post.objects.create(
            username=self.user,
            post_content='This is a test review post',
            tag_id=self.tag,
            subject=self.subject,
            post_date=timezone.now()
        )

        # Create a profile for the user
        # Profile.objects.create(
        #     user=self.user,
        #     biography='Test biography',
        #     display_photo='path/to/test/photo.jpg'
        # )

    def test_review_hub_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the review hub view
        response = self.client.get(reverse('kuhub:review'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'kuhub/review.html')

        # Check if the correct context variables are present
        self.assertIn('posts_list', response.context)
        self.assertIn('like_icon_styles', response.context)
        self.assertIn('dislike_icon_styles', response.context)
        self.assertIn('profiles_list', response.context)
        self.assertIn('form', response.context)

        # Check if the review post is in the context
        self.assertIn(self.review_post, response.context['posts_list'])

    def test_review_hub_view_no_authenticated_user(self):
        # Access the review hub view without logging in
        response = self.client.get(reverse('kuhub:review'))

        # Check if the response lets the user stay on the page
        self.assertRedirects(response, 200)
