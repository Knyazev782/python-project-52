from django.test import TestCase, Client
from django.urls import reverse
from task_manager.users.models import Users

class CrudUsersTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Users.objects.create_user(username='testuser', password='12345')
        self.another_user = Users.objects.create_user(username='anotheruser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.custom_user = self.user
        self.another_custom_user = self.another_user

    def test_create_user(self):
        response = self.client.post(reverse('create_user'), {
            'username': 'newuser123',
            'password1': '12345',
            'password2': '12345',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Users.objects.count(), 2)

    def test_list_users(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')

    def test_update_own_user(self):
        url_path = reverse('update_user', kwargs={'pk': self.custom_user.id})
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_update.html')

    def test_update_another_user(self):
        url_path = reverse('update_user', kwargs={'pk': self.another_custom_user.id})
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Вы можете изменять только себя.")

    def test_delete_own_user(self):
        url_path = reverse('delete_user', kwargs={'pk': self.custom_user.id})
        response = self.client.post(url_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        self.assertEqual(Users.objects.count(), 1)

    def test_delete_another_user(self):
        url_path = reverse('delete_user', kwargs={'pk': self.another_custom_user.id})
        response = self.client.post(url_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Вы можете удалять только себя.")

    # test_protected_user
    # def test_protected_user(self):
    #     with self.assertRaises(IntegrityError):
    #         self.custom_user.delete()

    def tearDown(self):
        self.client.logout()
        Users.objects.all().delete()