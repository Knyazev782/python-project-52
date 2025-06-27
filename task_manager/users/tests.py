from django.test import TestCase, Client
from django.urls import reverse
from task_manager.users.models import Users
from task_manager.tasks.models import Tasks
from task_manager.statuses.models import Statuses


class CrudUsersTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Users.objects.create_user(
            username='testuser',
            password='12345',
            first_name='Test',
            last_name='User'
        )
        self.another_user = Users.objects.create_user(
            username='anotheruser',
            password='12345',
            first_name='Another',
            last_name='User'
        )
        self.status = Statuses.objects.create(name='In Progress')
        self.task = Tasks.objects.create(
            name='Task1',
            description='Desc1',
            author=self.user,
            status=self.status,
            assigned_to=self.user
        )
        self.client.login(username='testuser', password='12345')

    def test_list_users(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'Test User')

    def test_create_user(self):
        self.assertEqual(Users.objects.count(), 2)
        response = self.client.post(reverse('create_user'), {
            'username': 'newuser123',
            'password1': '12345',
            'password2': '12345',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Users.objects.count(), 3)
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'Пользователь успешно зарегистрирован')

    def test_update_own_user(self):
        url_path = reverse('update_user', kwargs={'pk': self.user.id})
        response = self.client.post(url_path, {
            'username': 'updateduser',
            'password1': '12345',
            'password2': '12345',
            'first_name': 'Updated',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        response = self.client.get(reverse('users'))
        self.assertContains(response, 'Пользователь успешно изменён')
        self.assertEqual(Users.objects.get(pk=self.user.id).username, 'updateduser')

    def test_update_another_user(self):
        url_path = reverse('update_user', kwargs={'pk': self.another_user.id})
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        response = self.client.get(reverse('users'))
        self.assertContains(response, 'Вы не можете редактировать других пользователей')

    def test_delete_own_user(self):
        user_to_delete = Users.objects.create_user(
            username='todelete',
            password='12345',
            first_name='To',
            last_name='Delete'
        )
        self.client.login(username='todelete', password='12345')
        url_path = reverse('delete_user', kwargs={'pk': user_to_delete.id})
        response = self.client.post(url_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        response = self.client.get(reverse('users'))
        self.assertContains(response, 'Пользователь успешно удалён')
        self.assertEqual(Users.objects.filter(username='todelete').count(), 0)

    def test_delete_another_user(self):
        url_path = reverse('delete_user', kwargs={'pk': self.another_user.id})
        response = self.client.post(url_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        response = self.client.get(reverse('users'))
        self.assertContains(response, 'Вы не можете удалять других пользователей')

    def test_delete_protected_user(self):
        url_path = reverse('delete_user', kwargs={'pk': self.user.id})
        response = self.client.post(url_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        response = self.client.get(reverse('users'))
        self.assertContains(response, 'Нельзя удалить пользователя, потому что он используется')

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/users/')

    def tearDown(self):
        self.client.logout()
        Tasks.objects.all().delete()
        Users.objects.all().delete()
        Statuses.objects.all().delete()
