from django.test import TestCase
from django.contrib.auth.models import User
from kuhub.models import Group, GroupTags, GroupPassword
import datetime
from django.utils import timezone

class GroupModelTest(TestCase):

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

        # Create GroupTags for testing
        self.group_tag1 = GroupTags.objects.create(tag_text='tag1')
        self.group_tag2 = GroupTags.objects.create(tag_text='tag2')

    def test_group_creation(self):
        # Create a Group instance
        group = Group.objects.create(
            group_name='Test Group',
            group_description='This is a test group',
            create_date=datetime.date.today(),
        )
        group.group_member.add(self.user1, self.user2)
        group.group_tags.add(self.group_tag1, self.group_tag2)

        # Check if the Group is created successfully
        self.assertIsInstance(group, Group)
        self.assertEqual(group.group_name, 'Test Group')
        self.assertEqual(group.group_description, 'This is a test group')
        self.assertEqual(group.group_member.count(), 2)
        self.assertEqual(group.group_tags.count(), 2)
        self.assertEqual(group.create_date, datetime.date.today())

    def test_was_published_recently_post(self):
        # Create a Group instance
        group = Group.objects.create(
            group_name='Test Group',
            group_description='This is a test group',
            create_date=datetime.date.today(),
        )

        # Check if the was_published_recently_post method works
        self.assertTrue(group.was_published_recently_post())

    def test_group_str_method(self):
        # Create a Group instance
        group = Group.objects.create(
            group_name='Test Group',
            group_description='This is a test group',
            create_date=datetime.date.today(),
        )

        # Check if the __str__ method returns the expected result
        self.assertEqual(str(group), 'Test Group')

    def test_group_with_password(self):
        # Create a GroupPassword instance
        group_password = GroupPassword.objects.create(group_password='testpassword')

        # Create a Group instance with a password
        group = Group.objects.create(
            group_name='Test Group',
            group_description='This is a test group',
            create_date=datetime.date.today(),
            group_password=group_password
        )

        # Check if the Group is created successfully with a password
        self.assertEqual(group.group_password, group_password)
