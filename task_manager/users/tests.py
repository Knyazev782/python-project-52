from django.test import TestCase, Client
from django.urls import reverse
from task_manager.users.models import Users


class CrudUsersTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Users.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            password='testpassword123'
        )
        self.client.login(username='testuser', password='testpassword123')

    def test_user_list(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')
        self.assertContains(response, 'Test User')

    def test_user_create(self):
        response = self.client.post(reverse('user_create'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Users.objects.filter(username='newuser').exists())

    def test_user_update(self):
        response = self.client.post(reverse('user_update', args=[self.user.pk]), {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_user_delete(self):
        response = self.client.post(reverse('user_delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Users.objects.filter(pk=self.user.pk).exists())

    def tearDown(self):
        self.client.logout()
