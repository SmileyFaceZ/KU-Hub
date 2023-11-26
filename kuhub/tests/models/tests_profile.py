from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.contrib.auth.models import User
from kuhub.models import Profile


class ProfileModelTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.user.save()

    def test_profile_creation(self):
        # Create a new user for this test
        new_user = User(
            username='testuser2',
            password='testpassword2'
        )
        new_user.save()

        # Create a Profile instance linked to the new user
        profile = get_object_or_404(Profile, user=new_user)
        profile.biography = 'This is a test biography'
        profile.display_photo = 'path/to/test/photo.jpg'

        # Check if the profile is created successfully
        self.assertIsInstance(profile, Profile)
        self.assertEqual(profile.user, new_user)
        self.assertEqual(profile.biography, 'This is a test biography')
        self.assertEqual(profile.display_photo, 'path/to/test/photo.jpg')

    def test_profile_str_method(self):
        # Create a new user for this test
        new_user = User.objects.create_user(
            username='testuser3',
            password='testpassword3'
        )

        # Create a Profile instance linked to the new user
        profile = get_object_or_404(Profile, user=new_user)

        # Check if the __str__ method returns the expected result
        self.assertEqual(str(profile), 'testuser3')
