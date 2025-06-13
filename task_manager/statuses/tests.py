from django.test import TestCase, Client
from django.urls import reverse
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses

class CrudStatusesTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Users.objects.create_user(username='testuser', password='12345')
        self.another_user = Users.objects.create_user(username='anotheruser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.status = Statuses.objects.create(name='Test Status', created_by=self.user)
        self.another_status = Statuses.objects.create(name='Another Status', created_by=self.another_user)

    def test_create_status(self):
        response = self.client.post(reverse('create_status'), {'name': 'New Status'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Statuses.objects.count(), 3)

    def test_list_statuses(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/statuses_list.html')

    def test_update_own_status(self):
        url_path = reverse('update_status', kwargs={'pk': self.status.id})
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update_status.html')

    def test_update_another_status(self):
        url_path = reverse('update_status', kwargs={'pk': self.another_status.id})
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Вы можете изменять только свои статусы.")

    def test_delete_own_status(self):
        url_path = reverse('delete_status', kwargs={'pk': self.status.id})
        response = self.client.post(url_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses'))
        self.assertEqual(Statuses.objects.count(), 1)

    def test_delete_another_status(self):
        url_path = reverse('delete_status', kwargs={'pk': self.another_status.id})
        response = self.client.post(url_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Вы можете удалять только свои статусы.")

    # test_protected_status, так как нет зависимостей
    # def test_protected_status(self):
    #     with self.assertRaises(IntegrityError):
    #         self.status.delete()

    def tearDown(self):
        self.client.logout()
        Users.objects.all().delete()
        Statuses.objects.all().delete()