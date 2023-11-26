from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from kuhub.models import Post, UserFollower, Profile, Tags, Subject
from kuhub.views import HomePageView


class HomePageViewTest(TestCase):

    def setUp(self):
        # Create users for testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.followed_user = User.objects.create_user(
            username='followeduser',
            password='followedpassword'
        )
        self.unfollowed_user = User.objects.create_user(
            username='unfolloweduser',
            password='unfollowedpassword'
        )

        self.tag = Tags()
        self.tag.save()
        self.subject = Subject()
        self.subject.save()

        # Create a post for the followed user
        self.followed_user_post = Post.objects.create(
            username=self.followed_user,
            post_content='This is a test post from the followed user',
            tag_id=self.tag,
            subject=self.subject
        )

        # Create a UserFollower instance for the logged-in user
        UserFollower.objects.create(
            user_followed=self.followed_user,
            follower=self.user
        )

        # Create a profile for the followed user
        # Profile.objects.create(
        #     user=self.followed_user,
        #     biography='Test biography',
        #     display_photo='path/to/test/photo.jpg',
        # )

    def test_home_page_view_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the home page view
        response = self.client.get(reverse('kuhub:home'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'kuhub/home_page.html')

        # Check if the correct context variables are present
        self.assertIn('followed_users_posts', response.context)
        self.assertIn('like_icon_styles', response.context)
        self.assertIn('dislike_icon_styles', response.context)
        self.assertIn('form', response.context)
        self.assertIn('profiles_list', response.context)

        # Check if the followed user's post is in the context
        self.assertIn(self.followed_user_post, response.context['followed_users_posts'])

    def test_home_page_view_unauthenticated_user(self):
        # Access the home page view without logging in
        response = self.client.get(reverse('kuhub:home'))

        # Check if the response redirects to the login page
        self.assertRedirects(response, f'/accounts/login/')

        # Check if the correct message is displayed
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Please log in to see posts from people you follow.")

    def test_home_page_view_no_followed_users(self):
        # Remove the follower relationship
        UserFollower.objects.filter(user_followed=self.followed_user, follower=self.user).delete()

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the home page view
        response = self.client.get(reverse('kuhub:home'))

        # Check if the correct message is displayed
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You are not following anyone yet.")

    def test_home_page_view_no_posts(self):
        # Remove the post from the followed user
        self.followed_user_post.delete()

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the home page view
        response = self.client.get(reverse('kuuhub:home'))

        # Check if the context contains an empty queryset
        self.assertQuerysetEqual(response.context['followed_users_posts'], [])

    def test_home_page_view_search_filter(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the home page view with search parameters
        response = self.client.get(reverse('kuhub:home'), {'search': 'test'})

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'kuhub/home_page.html')

        # Check if the correct context variables are present
        self.assertIn('followed_users_posts', response.context)
        self.assertIn('like_icon_styles', response.context)
        self.assertIn('dislike_icon_styles', response.context)
        self.assertIn('form', response.context)
        self.assertIn('profiles_list', response.context)

        # Check if the followed user's post is still in the context
        self.assertIn(self.followed_user_post, response.context['followed_users_posts'])

    def test_home_page_view_no_authenticated_user(self):
        # Access the home page view without logging in
        response = self.client.get(reverse('kuhub:home'))

        # Check if the response redirects to the login page
        self.assertRedirects(response, f'/accounts/login/')
