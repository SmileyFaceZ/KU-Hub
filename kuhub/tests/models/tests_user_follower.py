from django.test import TestCase
from django.contrib.auth.models import User
from kuhub.models import UserFollower


class UserFollowerModelTest(TestCase):

    def setUp(self):
        # Create users for testing
        self.user1 = User.objects.create_user(
            username='user1',
            password='password1'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password2'
        )
        self.user3 = User.objects.create_user(
            username='user3',
            password='password3'
        )

    def test_user_follower_creation(self):
        # Create a UserFollower instance
        user_follower = UserFollower.objects.create(
            user_followed=self.user1,
            follower=self.user2,
            follow_date='2023-01-01 12:00:00'
        )

        # Check if the UserFollower is created successfully
        self.assertIsInstance(user_follower, UserFollower)
        self.assertEqual(user_follower.user_followed, self.user1)
        self.assertEqual(user_follower.follower, self.user2)
        self.assertEqual(str(user_follower.follow_date), '2023-01-01 12:00:00')

    def test_related_name(self):
        # Create a UserFollower instance
        user_follower = UserFollower(
            user_followed=self.user1,
            follower=self.user2,
            follow_date='2023-01-01 12:00:00'
        )
        user_follower.save()
        user_follower2 = UserFollower(
            user_followed=self.user1,
            follower=self.user3,
            follow_date='2023-01-01 12:00:00'
        )
        user_follower2.save()

        # Check if the related name 'follower' works
        followers = UserFollower.objects.filter(user_followed=self.user1)
        self.assertEqual(followers.count(), 2)
        self.assertEqual(followers.first().follower.username, self.user2.username)
