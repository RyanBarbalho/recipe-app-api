"""tests for django admin modifications"""
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)  # force_login is a helper function that allows you to log a user in without having to manually log them in. # noqa
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='password123',
            name='Test user'
        )

    def test_users_listed(self):
        """test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')  # reverse is a helper function that generates the URL for the Django admin page # noqa
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
