"""Import module tests from django."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class UserAuthTest(TestCase):
    """Tests for authenticated users."""

    def setUp(self):
        """Set up method for user tests."""
        self.client = Client()
        self.username = "testuser"
        self.password = "testpassword1234"
        self.gmail = "testuser@gmail.com"
        self.user = User.objects.create_user(
            username=self.username,
            email=self.gmail,
            password=self.password
        )

    def test_login(self):
        """Authenticated users can log in."""
        response = self.client.post(reverse('account_login'), {
            'login': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)
        self.assertEqual(self.client.session['_auth_user_id'], str(self.user.id))
        self.assertRedirects(response, reverse('kuhub:review'))
