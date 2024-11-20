from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class UserModelTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            password='securepassword',
            email='testuser@example.com',
            first_name='Test',
            last_name='User'
        )

    def test_create_user(self):
        """Test that the user is created successfully."""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('securepassword'))
        self.assertFalse(self.user.is_staff)  # By default, users are not staff
        self.assertFalse(self.user.is_superuser)  # By default, users are not superusers
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')

    def test_user_string_representation(self):
        """Test the string representation of the user."""
        self.assertEqual(str(self.user), 'testuser')

    def test_get_full_name(self):
        """Test the full name retrieval (should be first + last name, but it's empty for now)."""
        self.assertEqual(self.user.get_full_name(), 'Test User')
    
    def test_get_short_name(self):
        """Test the short name retrieval (should return username)."""
        self.assertEqual(self.user.get_short_name(), 'Test')

    def test_user_permissions(self):
        """Test user permissions and group membership."""
        # Test that user has no permissions by default
        self.assertFalse(self.user.has_perm('some_permission'))

        # Add permission via group or directly
        self.user.is_staff = True
        self.user.save()

        self.assertTrue(self.user.is_staff)  # Now the user is staff

    def test_user_login(self):
        """Test user authentication and login."""
        # Log in the user and check if the login is successful
        self.client.login(username='testuser', password='securepassword')
        response = self.client.get(reverse('index'))  # Use a valid URL for your project
        self.assertEqual(response.status_code, 200)
