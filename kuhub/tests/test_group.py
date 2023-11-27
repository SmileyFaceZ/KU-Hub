"""Import module tests from django."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from kuhub.models import Group, GroupEvent, GroupPassword, Task, GroupTags


class GroupTest(TestCase):
    """Tests for Group feature."""

    def setUp(self):
        """Set up method for user tests."""
        self.client = Client()
        # first user
        self.username1 = "testuser1"
        self.password1 = "testpassword1234"
        self.gmail1 = "testuser1@gmail.com"
        self.user1 = User.objects.create_user(
            username=self.username1,
            email=self.gmail1,
            password=self.password1
        )
        #second user
        self.username2 = "testuser2"
        self.password2 = "testpassword1234"
        self.gmail2 = "testuser2@gmail.com"
        self.user2 = User.objects.create_user(
            username=self.username2,
            email=self.gmail2,
            password=self.password2
        )
        #set up group
        self.group1 = Group.objects.create(
            group_name='group1',
            group_description='test',
        )

    def login(self, user: User):
        """
        Utility function to 'login' a user to the Client session.
        This is needed in many tests.
        """
        # "login" the user to the client session
        if user == self.user1:
            self.assertTrue( self.client.login(
                        username=self.username1, password=self.password1) )
        elif user == self.user2:
            self.assertTrue( self.client.login(
                        username=self.username2, password=self.password2) )
        else:
            self.fail(f"login: Unrecognized user parameter {user.username}")

    def test_join_without_login(self):
        """
        Anonymous user can't join group. Join button will redircect to login page instead
        """
        url = reverse('kuhub:join', args=[self.group1.id])
        response = self.client.post(url)
        # Reverse the login URL provided by Allauth
        expected_redirect_url = reverse('account_login')+ f"?next={url}"
        # Check if redirect to login page
        self.assertRedirects(response, expected_redirect_url)

    def test_join_but_already_be_a_member(self):
        """
        User who already in group
        """
        url = reverse('kuhub:join', args=[self.group1.id])
        self.group1.group_member.add(self.user1)
        self.login(self.user1)
        response = self.client.post(url)
        # Check if redirect to login page
        self.assertRedirects(response, reverse('kuhub:'))